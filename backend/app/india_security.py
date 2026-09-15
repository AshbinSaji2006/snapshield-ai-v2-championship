"""Original curated multilingual patterns; no multilingual classifier accuracy claim."""
import re

PATTERNS=[
    ("INDIA_CREDENTIAL","Authentication information requested",r"(?:otp|ओटीपी|password|पासवर्ड|pin|पिन).{0,35}(?:bhej|bata|share|do\b|भेज|बता|साझा)|(?:bhej|bata|भेज|बता|साझा).{0,35}(?:otp|ओटीपी|password|पासवर्ड|pin|पिन)",24),
    ("INDIA_KYC","KYC pressure with requested action",r"(?:kyc|केवाईसी).{0,60}(?:expire|block|band|बंद|बन्द|रोक).{0,80}(?:link|click|otp|लिंक|क्लिक|ओटीपी)",18),
    ("INDIA_DISCONNECT","Disconnection pressure with payment/link",r"(?:electricity|bijli|बिजली).{0,65}(?:disconnect|kat|कट|बंद).{0,80}(?:pay|payment|link|भुगतान|लिंक)",20),
    ("INDIA_ARREST","Digital-arrest payment or isolation demand",r"(?:digital arrest|डिजिटल अरेस्ट|police|पुलिस).{0,100}(?:transfer|payment|जमा|भेज|secrecy|do not tell|किसी को)",24),
    ("INDIA_UPI","UPI PIN requested to receive money",r"(?:refund|receive|रिफंड|प्राप्त).{0,80}(?:upi|यूपीआई).{0,35}(?:pin|पिन)",24),
    ("INDIA_JOB","Recruitment payment demand",r"(?:job|recruit|नौकरी|hiring).{0,80}(?:registration fee|security deposit|pay.{0,15}fee|जमा|शुल्क)",18),
    ("INDIA_PARCEL","Customs parcel payment pressure",r"(?:parcel|पार्सल).{0,70}(?:(?:customs|कस्टम).{0,40}(?:hold|held|रोक)|(?:hold|held|रोक).{0,40}(?:customs|कस्टम)).{0,70}(?:pay|fee|भुगतान)",18),
]

def india_signals(text):
    # Negation applies locally to matched request, not as a global whitelist.
    findings=[]
    for code,name,pattern,points in PATTERNS:
        for match in re.finditer(pattern,text,re.I):
            context=text[max(0,match.start()-30):min(len(text),match.end()+15)]
            if code != "INDIA_ARREST" and re.search(r"never|do not|don't|mat\s+(?:bhej|bata|do)|नहीं|मत\s",context,re.I): continue
            findings.append({"id":code,"name":name,"severity":"high","description":"Combined request and pressure patterns warrant independent verification; this is a curated deterministic check.","contribution":points,"evidence":match.group()[:90],"provenance":"normalized security text"})
            break
    return findings
