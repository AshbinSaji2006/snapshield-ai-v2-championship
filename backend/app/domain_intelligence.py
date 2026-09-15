"""Offline PSL parsing and explainable hostname facts. Never performs DNS or HTTP."""
from functools import lru_cache
from pathlib import Path
import ipaddress
import unicodedata
from .normalization import CONFUSABLES

@lru_cache(maxsize=1)
def suffix_rules():
    path=Path(__file__).resolve().parents[1]/"resources/public_suffix_list.dat"
    exact,wild,exceptions=set(),set(),set()
    for line in path.read_text(encoding="utf-8").splitlines():
        rule=line.strip()
        if not rule or rule.startswith("//"): continue
        target=exceptions if rule.startswith("!") else wild if rule.startswith("*.") else exact
        target.add(rule.removeprefix("!").removeprefix("*.").encode("idna").decode("ascii"))
    return exact,wild,exceptions

def domain_facts(host):
    host=host.rstrip(".").lower()
    try:
        ipaddress.ip_address(host)
        return {"host":host,"registrable_domain":host,"is_ip":True,"unicode_host":host,"confusable_skeleton":host,"mixed_script":False,"psl_available":True}
    except ValueError: pass
    try:
        ascii_host=host.encode("idna").decode("ascii")
    except UnicodeError:
        # Preserve a bounded, non-navigable representation for malformed OCR/text.
        safe_host="".join(c if c.isascii() and (c.isalnum() or c in ".-") else "?" for c in host)[:253]
        return {"host":safe_host,"registrable_domain":safe_host,"is_ip":False,"unicode_host":host[:253],
                "confusable_skeleton":host.translate(CONFUSABLES)[:253],"mixed_script":False,
                "psl_available":True,"idna_valid":False}
    try: unicode_host=ascii_host.encode("ascii").decode("idna")
    except UnicodeError: unicode_host=host
    labels=ascii_host.split("."); suffix_count=1
    available=True
    try:
        exact,wild,exceptions=suffix_rules()
        for i in range(len(labels)):
            tail=".".join(labels[i:])
            if tail in exceptions:
                suffix_count=len(labels)-i-1; break
            if tail in exact: suffix_count=max(suffix_count,len(labels)-i)
            if i+1<len(labels) and ".".join(labels[i+1:]) in wild:
                suffix_count=max(suffix_count,len(labels)-i)
    except OSError: available=False
    registrable=".".join(labels[-(suffix_count+1):])
    scripts=set()
    for c in unicode_host:
        if c.isalpha():
            scripts.add(unicodedata.name(c,"").split(" ")[0])
    return {"host":ascii_host,"registrable_domain":registrable,"is_ip":False,"unicode_host":unicode_host,
            "confusable_skeleton":unicode_host.translate(CONFUSABLES),"mixed_script":len(scripts)>1,"psl_available":available,"idna_valid":True}

def edit_distance(a,b):
    if abs(len(a)-len(b))>2: return 3
    previous=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        current=[i]
        for j,cb in enumerate(b,1): current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+(ca!=cb)))
        previous=current
    return previous[-1]
