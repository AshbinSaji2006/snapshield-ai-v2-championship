"""Reproducible tournament. Selection/calibration are disjoint; test is not read here."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import time

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("HF_HOME", str(ROOT / ".cache/huggingface"))
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np
import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import HfApi, snapshot_download
from safetensors.torch import save_file, load_file
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, f1_score, confusion_matrix, roc_auc_score, average_precision_score, brier_score_loss
from sklearn.model_selection import train_test_split
from scipy.optimize import minimize_scalar

CANDIDATES = {
    "bert_tiny": ("google/bert_uncased_L-2_H-128_A-2", "30b0a37ccaaa32f332884b96992754e246e48c5f", 5e-5),
    "minilm_l6": ("sentence-transformers/all-MiniLM-L6-v2", "1110a243fdf4706b3f48f1d95db1a4f5529b4d41", 2e-5),
    "distilbert": ("distilbert/distilbert-base-uncased", None, 2e-5),
}

def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def read_split(name):
    rows = (ROOT / f"data/processed/uci_sms/{name}.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return [r.split("\t", 1)[1] for r in rows], np.array([int(r.split("\t", 1)[0]) for r in rows])

def metrics(y, p):
    pred = np.asarray(p) >= .5
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    precision, recall, f1, _ = precision_recall_fscore_support(y, pred, average="binary", zero_division=0)
    bins = []
    ece = 0.
    for lower in np.arange(0, 1, .1):
        mask = (p >= lower) & (p < lower + .1 if lower < .9 else p <= 1)
        if mask.any():
            observed, forecast = float(y[mask].mean()), float(p[mask].mean())
            ece += mask.mean() * abs(observed - forecast)
            bins.append({"lower": float(lower), "count": int(mask.sum()), "observed_positive_rate": observed, "mean_probability": forecast})
    return {"n": len(y), "accuracy": float(accuracy_score(y, pred)), "precision": float(precision),
            "recall": float(recall), "f1": float(f1), "macro_f1": float(f1_score(y, pred, average="macro")),
            "fpr": float(fp / max(1, tn+fp)), "fnr": float(fn / max(1, tp+fn)),
            "pr_auc": float(average_precision_score(y, p)) if y.any() else None,
            "roc_auc": float(roc_auc_score(y, p)) if len(set(y)) == 2 else None,
            "brier": float(brier_score_loss(y, p)), "ece_10_bins": float(ece),
            "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]], "reliability_bins": bins}

def selection_score(m):
    return .45*m["recall"] + .35*m["macro_f1"] - .20*m["fpr"]

class SecurityEncoder(nn.Module):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder
        self.head = nn.Linear(encoder.config.hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        hidden = self.encoder(input_ids=input_ids.long(), attention_mask=attention_mask.long()).last_hidden_state
        mask = attention_mask.unsqueeze(-1).to(hidden.dtype)
        pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1)
        return self.head(pooled).squeeze(-1)

def predict(model, inputs, device, batch=32):
    model.eval()
    values = []
    with torch.inference_mode():
        for start in range(0, len(inputs["input_ids"]), batch):
            data = {k: v[start:start+batch].to(device) for k,v in inputs.items() if k in {"input_ids", "attention_mask"}}
            values.extend(model(**data).float().cpu().numpy().tolist())
    return np.asarray(values)

def sigmoid(logit):
    return 1 / (1 + np.exp(-np.clip(logit, -50, 50)))

def run_candidate(name, epochs=4):
    identifier, revision, lr = CANDIDATES[name]
    out = ROOT / f"ml/v2/experiments/{name}"
    out.mkdir(parents=True, exist_ok=True)
    if (out / "experiment.json").exists():
        print(f"Already completed {name}; retaining recorded run.", flush=True); return
    meta = HfApi().model_info(identifier, revision=revision)
    license_name = (meta.card_data or {}).get("license")
    if license_name != "apache-2.0":
        raise ValueError(f"Review model license: {license_name}")
    revision = meta.sha
    cached = snapshot_download(identifier, revision=revision, allow_patterns=["config.json", "model.safetensors", "vocab.txt", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "README.md", "LICENSE*"])
    if not (Path(cached)/"model.safetensors").exists():
        raise ValueError("Safe tensor weights unavailable; pickle weights not loaded")
    random.seed(42); np.random.seed(42); torch.manual_seed(42)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)
    torch.set_num_threads(4)
    torch.backends.cudnn.deterministic = True; torch.backends.cudnn.benchmark = False
    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_x, train_y = read_split("train")
    val_x, val_y = read_split("validation")
    selection, calibration = train_test_split(np.arange(len(val_y)), test_size=.5, stratify=val_y, random_state=42)
    tokenizer = AutoTokenizer.from_pretrained(cached, local_files_only=True, trust_remote_code=False)
    # Tiny's original vocabulary lacks tokenizer metadata; infer via explicit Bert tokenizer if needed.
    train_inputs = tokenizer(train_x, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
    val_inputs = tokenizer(val_x, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
    encoder = AutoModel.from_pretrained(cached, local_files_only=True, trust_remote_code=False, use_safetensors=True, attn_implementation="eager")
    model = SecurityEncoder(encoder).to(device)
    optimizer = torch.optim.AdamW([{"params": model.encoder.parameters(), "lr": lr}, {"params": model.head.parameters(), "lr": 1e-3}], weight_decay=.01)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor(2., device=device))
    generator = torch.Generator().manual_seed(42)
    curves = []
    best = -1.
    began = time.perf_counter()
    for epoch in range(epochs):
        model.train(); losses = []
        indices = torch.randperm(len(train_y), generator=generator)
        for step in range(0, len(indices), 16):
            idx = indices[step:step+16]
            inputs = {k: v[idx].to(device) for k,v in train_inputs.items() if k in {"input_ids", "attention_mask"}}
            labels = torch.tensor(train_y[idx.numpy()], dtype=torch.float32, device=device)
            optimizer.zero_grad(set_to_none=True)
            loss = loss_fn(model(**inputs), labels); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
            optimizer.step(); losses.append(float(loss.detach()))
        logits = predict(model, val_inputs, device)
        m = metrics(val_y[selection], sigmoid(logits[selection]))
        score = selection_score(m) if m["fpr"] <= .02 else -1
        curves.append({"epoch": epoch+1, "loss": float(np.mean(losses)), "selection": m, "selection_score": score})
        print(json.dumps({"candidate": name, "epoch": epoch+1, "recall": m["recall"], "fpr": m["fpr"], "score": score}), flush=True)
        if score > best or epoch == 0:
            best = score
            save_file({k:v.detach().cpu().contiguous() for k,v in model.state_dict().items()}, str(out/"weights.safetensors"))
    model.load_state_dict(load_file(str(out/"weights.safetensors")))
    logits = predict(model, val_inputs, device)
    cal_logits = logits[calibration]
    temperature = float(minimize_scalar(lambda t: float(np.mean(np.logaddexp(0,cal_logits/t) - val_y[calibration]*cal_logits/t)), bounds=(.5,5), method="bounded").x)
    # Temperature preserves the fixed 0.5 class boundary. Evaluation is on the disjoint selection partition.
    model.to("cpu").eval()
    example = (torch.ones((1,128), dtype=torch.int32), torch.ones((1,128), dtype=torch.int32))
    torch.onnx.export(model, example, str(out/"model.onnx"), input_names=["input_ids","attention_mask"], output_names=["logit"], opset_version=17, do_constant_folding=True)
    tokenizer.save_pretrained(out/"tokenizer")
    encoder.config.save_pretrained(out/"encoder_config")
    import onnxruntime as ort
    opts = ort.SessionOptions(); opts.intra_op_num_threads=4; opts.inter_op_num_threads=1
    session = ort.InferenceSession(str(out/"model.onnx"), sess_options=opts, providers=["CPUExecutionProvider"])
    onnx_logits=[]; timings=[]
    for i in range(len(val_y)):
        inputs={k: v[i:i+1].numpy().astype(np.int32) for k,v in val_inputs.items() if k in {"input_ids","attention_mask"}}
        t=time.perf_counter(); onnx_logits.append(float(session.run(None,inputs)[0].ravel()[0])); timings.append((time.perf_counter()-t)*1000)
    delta=float(np.max(np.abs(sigmoid(np.array(onnx_logits)/temperature)-sigmoid(logits/temperature))))
    agreement=float(np.mean((np.array(onnx_logits)>=0)==(logits>=0)))
    report={"experiment_id":name+"-seed42-v1", "candidate":name, "upstream":identifier,"revision":revision,"license":license_name,
            "upstream_weights_sha256":sha(Path(cached)/"model.safetensors"), "seed":42,"training_hardware":torch.cuda.get_device_name(0) if device=="cuda" else "CPU",
            "train_count":len(train_y), "selection_count":len(selection),"calibration_count":len(calibration),"test_read":False,
            "split_hashes":{n:sha(ROOT/f"data/processed/uci_sms/{n}.tsv") for n in ("train","validation")},
            "selection_indices":selection.tolist(),"calibration_indices":calibration.tolist(),"curves":curves,
            "selection":metrics(val_y[selection],sigmoid(logits[selection]/temperature)),"temperature":temperature,
            "calibration_evaluation_raw":metrics(val_y[selection],sigmoid(logits[selection])),
            "calibration_evaluation_scaled":metrics(val_y[selection],sigmoid(logits[selection]/temperature)),
            "parameters":sum(p.numel() for p in model.parameters()),"max_length":128,"batch_size":16,"epochs":epochs,
            "encoder_learning_rate":lr,"head_learning_rate":1e-3,"positive_weight":2.,"training_seconds":time.perf_counter()-began,
            "onnx_sha256":sha(out/"model.onnx"),"onnx_bytes":(out/"model.onnx").stat().st_size,"opset":17,
            "onnx_validation":{"n":len(val_y),"class_agreement":agreement,"max_probability_delta":delta},
            "cpu_inference_ms":{"median":float(np.median(timings[5:])),"p95":float(np.percentile(timings[5:],95)),"warmup":5,"repetitions":len(timings)-5,"threads":4},
            "versions":{p:importlib.metadata.version(p) for p in ("torch","transformers","onnx","onnxruntime","numpy","scikit-learn")}}
    (out/"experiment.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    np.savez_compressed(out/"validation_predictions.npz",labels=val_y,logits=logits,onnx_logits=np.array(onnx_logits))
    print(f"Completed {name}: ONNX agreement {agreement}, {report['cpu_inference_ms']}",flush=True)
    del model,encoder,session
    if device=="cuda": torch.cuda.empty_cache()

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--candidate",choices=[*CANDIDATES,"all"],default="all"); parser.add_argument("--epochs",type=int,default=4)
    args=parser.parse_args()
    for name in (CANDIDATES if args.candidate=="all" else [args.candidate]):
        try: run_candidate(name,args.epochs)
        except Exception as exc:
            out=ROOT/f"ml/v2/experiments/{name}"; out.mkdir(parents=True,exist_ok=True)
            (out/"failure.json").write_text(json.dumps({"type":type(exc).__name__,"message":str(exc),"status":"FAILED"},indent=2),encoding="utf-8")
            print(f"Candidate {name} failed: {type(exc).__name__}: {exc}",flush=True)
            if args.candidate != "all": raise

if __name__=="__main__": main()
