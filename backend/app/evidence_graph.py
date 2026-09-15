"""Deterministic evidence correlation with source attribution, not causal inference."""
import hashlib
import json
from urllib.parse import urlsplit
from .pii_analyzer import analyze_pii

def build_graph(result, sources):
    nodes={}; edges={}
    def node(kind,label,key,**detail):
        identifier=hashlib.sha256(f"{kind}:{key}".encode("utf-8",errors="replace")).hexdigest()[:16]
        safe_label=analyze_pii(str(label))[1]
        nodes[identifier]={"id":identifier,"type":kind,"label":safe_label[:100],"details":detail}
        return identifier
    def edge(a,b,relation):
        identifier=f"{a}:{relation}:{b}"
        edges[identifier]={"id":identifier,"source":a,"target":b,"type":relation}
    root=node("Input",result["input_type"].title()+" input","input",persisted=False)
    source_nodes=[]
    for i,source in enumerate(sources):
        kind=source.get("kind","TextEvidence")
        sid=node(kind,source.get("label",kind),str(i),provenance=kind,confidence=source.get("confidence"))
        edge(root,sid,"contains"); source_nodes.append((sid,source.get("text","")))
    decision=node("RiskDecision",f'{result["severity"].upper()} / {result["risk_score"]}',"decision",risk_score=result["risk_score"],score_type="ordinal evidence index, not probability")
    url_nodes={}; domain_nodes={}
    for i,url in enumerate(result["detected_urls"][:10]):
        # Node IDs do not disclose a hash of secret URL paths; only safe ordinal keys.
        uid=node("URL",analyze_pii(url)[1],str(i),navigated=False)
        url_nodes[url]=uid
        for sid,text in source_nodes:
            from .normalization import normalize_security
            if url in text or url in normalize_security(text).normalized_security_text: edge(sid,uid,"references")
        try: host=urlsplit(url).hostname or "unknown"
        except ValueError: host="unparseable"
        did=node("Domain",host,host); domain_nodes[host]=did; edge(uid,did,"has_hostname")
    for i,signal in enumerate(sorted(result["signals"],key=lambda x:-x["contribution"])[:24]):
        sid=node("MLFinding" if "ML" in signal["id"] or "DEEP" in signal["id"] else "RuleFinding",signal["name"],f'{signal["id"]}:{i}',
                 signal_id=signal["id"],description=signal["description"],risk_contribution=signal["contribution"],
                 evidence=analyze_pii(str(signal.get("evidence") or ""))[1],provenance=signal.get("provenance","combined local evidence"))
        edge(sid,decision,"increases_risk" if signal["contribution"]>0 else "corroborates")
        if signal["id"]=="BRAND_DOMAIN_MISMATCH":
            brand=node("ClaimedBrand",signal.get("brand","Claimed brand"),signal.get("brand","brand"))
            observed=domain_nodes.get(signal.get("observed_domain"))
            for source_id,text in source_nodes:
                if signal.get("brand","").lower() in text.lower(): edge(source_id,brand,"claims_brand")
            expected=node("ExpectedBrandDomain",", ".join(signal.get("expected_domains",[])),signal.get("brand","brand"))
            edge(brand,expected,"expects_domain")
            if observed: edge(observed,expected,"conflicts_with"); edge(observed,sid,"produced_by_check")
            edge(brand,sid,"corroborates")
        else:
            edge(root,sid,"produced_by_check")
    routing=result.get("details",{}).get("routing",{})
    route=node("RoutingDecision",routing.get("path","fast"),"routing",reasons=routing.get("reasons",[]))
    edge(root,route,"routed_to"); edge(route,decision,"informs")
    return {"schema_version":"2.0","nodes":list(nodes.values()),"edges":list(edges.values()),
            "description":"Evidence correlation graph; links indicate extraction and rule relationships, not proof of malicious intent",
            "truncated_signals":max(0,len(result["signals"])-24)}

def sanitized_export(incident):
    allow=("id","created_at","input_type","threat_score","severity","threat_category","classification","indicator_count","processing_time_ms","runtime_provider","sanitized_summary","model_version","evidence")
    return {"schema_version":"snapshield-incident-2","privacy":"No source content, URL, input hash or extracted PII included",
            "incident":{key:incident[key] for key in allow if key in incident}}
