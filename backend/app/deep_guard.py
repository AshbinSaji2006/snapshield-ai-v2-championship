"""Optional, hash-gated ONNX encoder. No network access or training-framework dependency."""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math
import time
import threading
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ARTIFACTS=ROOT/"ml/v2/deep_guard"

class DeepGuard:
    def __init__(self, directory=ARTIFACTS):
        self.ready=False; self.reason="No Deep Guard artifact passed the deployment gate"; self.provider="unavailable"
        self.manifest={}; self._lock=threading.Lock()
        try:
            manifest=json.loads((directory/"manifest.json").read_text(encoding="utf-8"))
            if manifest.get("deployment_approved") is not True: return
            for name,digest in manifest["file_hashes"].items():
                path=(directory/name).resolve()
                if not path.is_relative_to(directory.resolve()) or not path.is_file(): raise ValueError("Invalid artifact path")
                with path.open("rb") as stream:
                    if hashlib.file_digest(stream,"sha256").hexdigest()!=digest: raise ValueError("Artifact hash mismatch")
            if not {"model.onnx","tokenizer.json"} <= set(manifest["file_hashes"]): raise ValueError("Incomplete artifact hash manifest")
            import onnxruntime as ort
            from tokenizers import Tokenizer
            from .runtime import runtime_manager
            self.tokenizer=Tokenizer.from_file(str(directory/"tokenizer.json"))
            self.tokenizer.enable_truncation(max_length=128)
            self.tokenizer.enable_padding(length=128,pad_id=0,pad_token="[PAD]")
            opts=ort.SessionOptions(); opts.intra_op_num_threads=4; opts.inter_op_num_threads=1
            model_path=directory/"model.onnx"; providers=["CPUExecutionProvider"]
            validation=runtime_manager.snapdragon_validation()
            compiled=ROOT/"reports/snapdragon/aihub/snapshield_deep_guard_xelite.onnx"
            if (validation.get("verified") is True and validation.get("execution_provider")=="QNNExecutionProvider"
                    and "QNNExecutionProvider" in ort.get_available_providers() and compiled.is_file()
                    and hashlib.sha256(compiled.read_bytes()).hexdigest()==validation.get("compiled_artifact_sha256")):
                qnn_opts=ort.SessionOptions(); qnn_opts.add_session_config_entry("session.disable_cpu_ep_fallback","1")
                try:
                    self.session=ort.InferenceSession(str(compiled),sess_options=qnn_opts,providers=[("QNNExecutionProvider",{"backend_type":"htp"})])
                    model_path=compiled
                except Exception:
                    self.session=ort.InferenceSession(str(model_path),sess_options=opts,providers=providers)
            else:
                self.session=ort.InferenceSession(str(model_path),sess_options=opts,providers=providers)
            self.manifest=manifest; self.provider=self.session.get_providers()[0]
            runtime_manager.record_model_provider(self.provider)
            self.ready=True; self.reason="Selected, calibrated ONNX model; Snapdragon hardware validation pending"
        except Exception as exc:
            self.reason=f"Deep Guard unavailable ({type(exc).__name__}); Fast Guard remains active"

    def predict(self,text):
        if not self.ready: return None
        try:
            with self._lock:
                start=time.perf_counter(); encoded=self.tokenizer.encode(text)
                pre_ms=(time.perf_counter()-start)*1000
                start=time.perf_counter()
                inputs={"input_ids":np.array([encoded.ids],dtype=np.int32),"attention_mask":np.array([encoded.attention_mask],dtype=np.int32)}
                logit=float(self.session.run(None,inputs)[0].ravel()[0])
                inference_ms=(time.perf_counter()-start)*1000
                p=1/(1+math.exp(-max(-50,min(50,logit/self.manifest.get("temperature",1)))))
                return {"probability":p,"provider":self.provider,"version":self.manifest["version"],"preprocessing_ms":pre_ms,"inference_ms":inference_ms,"truncated":bool(encoded.overflowing)}
        except Exception:
            return None

    def status(self):
        return {"ready":self.ready,"provider":self.provider,"reason":self.reason,"version":self.manifest.get("version"),"model_name":self.manifest.get("model_name"),"snapdragon_npu_verified":False}

@lru_cache(maxsize=1)
def get_deep_guard(): return DeepGuard()

@lru_cache(maxsize=1)
def calibration_config():
    try: return json.loads((ROOT/"ml/v2/fast_calibration.json").read_text(encoding="utf-8"))
    except (OSError,ValueError): return {}

def calibrated_fast(probability):
    if probability is None: return None
    config=calibration_config()
    if not config.get("approved"): return probability
    p=min(max(probability,1e-8),1-1e-8)
    logit=math.log(p/(1-p))*config["coefficient"]+config["intercept"]
    return 1/(1+math.exp(-max(-50,min(50,logit))))
