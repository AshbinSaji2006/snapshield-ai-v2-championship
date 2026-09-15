"""Categorize Fast/Deep errors without publishing message bodies."""
from __future__ import annotations
from collections import Counter
import json, math, re
from pathlib import Path
import joblib, numpy as np, onnxruntime as ort
from tokenizers import Tokenizer

ROOT=Path(__file__).resolve().parents[2]

def categories(text):
    rules=[("bank_impersonation",r"bank|account|kyc|sbi"),("prize_lure",r"prize|won|reward|free|claim"),("promotion",r"sale|offer|discount|subscribe"),("url_heavy",r"https?://|www\.|hxxp|\.com"),("urgency",r"urgent|immediately|now|today|expire|suspend|block"),("financial_solicitation",r"pay|payment|cash|money|fee|credit|loan"),("credential_request",r"password|otp|pin|login|verify"),("delivery_customs",r"parcel|delivery|customs"),("short_ambiguous",r"^.{0,45}$")]
    found=[name for name,pattern in rules if re.search(pattern,text,re.I)]
    return found or ["other_ambiguous"]

def read_tsv():
    rows=(ROOT/"data/processed/uci_sms/test.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return [r.split("\t",1)[1] for r in rows],np.array([int(r.split("\t",1)[0]) for r in rows]),list(range(len(rows)))

def predictors(texts):
    v=joblib.load(ROOT/"ml/artifacts/text_vectorizer.joblib"); m=joblib.load(ROOT/"ml/artifacts/text_classifier.joblib")
    f=m.predict_proba(v.transform(texts))[:,1]
    c=json.loads((ROOT/"ml/v2/fast_calibration.json").read_text()); logit=np.log(np.clip(f,1e-8,1-1e-8)/np.clip(1-f,1e-8,1)); f=1/(1+np.exp(-np.clip(logit*c["coefficient"]+c["intercept"],-50,50)))
    manifest=json.loads((ROOT/"ml/v2/deep_guard/manifest.json").read_text()); tok=Tokenizer.from_file(str(ROOT/"ml/v2/deep_guard/tokenizer.json")); tok.enable_truncation(max_length=128); tok.enable_padding(length=128,pad_id=0,pad_token="[PAD]")
    opts=ort.SessionOptions(); opts.intra_op_num_threads=4; session=ort.InferenceSession(str(ROOT/"ml/v2/deep_guard/model.onnx"),sess_options=opts,providers=["CPUExecutionProvider"]); d=[]
    for text in texts:
        e=tok.encode(text); z=float(session.run(None,{"input_ids":np.array([e.ids],np.int32),"attention_mask":np.array([e.attention_mask],np.int32)})[0].ravel()[0]); d.append(1/(1+math.exp(-max(-50,min(50,z/manifest["temperature"])))))
    return f,np.array(d)

def analyze(name,texts,labels,identifiers):
    fast,deep=predictors(texts); output={}
    for model,p in (("fast_guard",fast),("deep_guard",deep)):
        errors=[]
        for i in np.where((p>=.5)!=labels)[0]: errors.append({"record":identifiers[i],"error":"false_positive" if labels[i]==0 else "false_negative","categories":categories(texts[i]),"probability":round(float(p[i]),6)})
        output[model]={"errors":len(errors),"false_negatives":sum(e["error"]=="false_negative" for e in errors),"false_positives":sum(e["error"]=="false_positive" for e in errors),"category_counts":dict(Counter(c for e in errors for c in e["categories"])),"records":errors}
    return output

def main():
    tx,ty,ti=read_tsv(); cross=json.loads((ROOT/"data/processed/cross_domain/mendeley_holdout.json").read_text(encoding="utf-8")); cx=[r["text"] for r in cross]; cy=np.array([r["label"] for r in cross]); ci=[r["source_row"] for r in cross]
    report={"schema_version":"1.0","privacy":"Dataset record indices and aggregate categories only; no message bodies","sets":{"uci_test":analyze("uci_test",tx,ty,ti),"cross_domain":analyze("cross_domain",cx,cy,ci)}}
    out=ROOT/"reports/v2/failure_analysis.json"; out.write_text(json.dumps(report,indent=2),encoding="utf-8"); print(json.dumps(report,indent=2))

if __name__=="__main__": main()
