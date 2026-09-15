"""Capture real v2 UI states through Edge DevTools; requires the local server."""
from __future__ import annotations
import argparse, base64, json, socket, subprocess, tempfile, time
from pathlib import Path
from urllib.request import urlopen
from websockets.sync.client import connect

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"docs/v2/assets/screenshots"
EDGE=Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--dashboard-only",action="store_true")
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1",0)); port=probe.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix="snapshield-edge-",ignore_cleanup_errors=True) as profile:
        proc=subprocess.Popen([str(EDGE),"--headless=new","--disable-gpu","--hide-scrollbars","--no-first-run","--window-size=1920,1080",f"--remote-debugging-port={port}","--remote-allow-origins=*",f"--user-data-dir={profile}","http://127.0.0.1:8766/"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            target=None
            for _ in range(60):
                try:
                    targets=json.load(urlopen(f"http://127.0.0.1:{port}/json",timeout=1)); target=next(t for t in targets if t.get("type")=="page"); break
                except Exception: time.sleep(.25)
            if not target: raise RuntimeError("Edge DevTools target unavailable")
            with connect(target["webSocketDebuggerUrl"],origin=f"http://127.0.0.1:{port}") as ws:
                seq=[0]
                def command(method,params=None):
                    seq[0]+=1; ident=seq[0]; ws.send(json.dumps({"id":ident,"method":method,"params":params or {}}))
                    while True:
                        reply=json.loads(ws.recv())
                        if reply.get("id")==ident:
                            if "error" in reply: raise RuntimeError(str(reply["error"]))
                            return reply.get("result",{})
                def evaluate(expression): return command("Runtime.evaluate",{"expression":expression,"awaitPromise":True,"returnByValue":True}).get("result",{}).get("value")
                def click(label):
                    script=f"(()=>{{const e=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().includes({json.dumps(label)}));if(!e)return false;e.click();return true}})()"
                    if not evaluate(script): raise RuntimeError(f"Button not found: {label}")
                    time.sleep(.5)
                def wait_for(selector,timeout=40):
                    end=time.time()+timeout
                    while time.time()<end:
                        if evaluate(f"Boolean(document.querySelector({json.dumps(selector)}))"): return
                        time.sleep(.4)
                    raise RuntimeError(f"Timed out waiting for {selector}")
                def wait_for_text(value,timeout=40):
                    end=time.time()+timeout
                    while time.time()<end:
                        if evaluate(f"document.body.innerText.includes({json.dumps(value)})"): return
                        time.sleep(.4)
                    raise RuntimeError(f"Timed out waiting for text: {value}")
                def shot(name):
                    evaluate("window.scrollTo(0,0);document.querySelectorAll('main,.content,.shell').forEach(e=>{e.scrollTop=0;e.scrollLeft=0})")
                    time.sleep(.25)
                    data=command("Page.captureScreenshot",{"format":"png","captureBeyondViewport":False,"fromSurface":True})["data"]
                    (OUT/name).write_bytes(base64.b64decode(data)); print(name,flush=True)
                command("Page.enable"); command("Runtime.enable"); wait_for(".hero-copy"); wait_for_text("CPUExecutionProvider")
                shot("01_command_center.png")
                if args.dashboard_only: return
                click("Analyze"); wait_for(".composer")
                click("Legitimate"); click("Analyze locally"); wait_for(".result-hero"); shot("02_legitimate_analysis.png")
                click("Bank phish"); click("Analyze locally"); wait_for(".result-hero"); shot("03_phishing_analysis.png")
                click("Screenshot"); time.sleep(1); click("Analyze locally"); wait_for(".extraction-card",timeout=120)
                evaluate("document.body.style.zoom='.85'"); shot("04_multimodal_analysis.png"); evaluate("document.body.style.zoom='1'")
                evaluate("document.querySelector('.graph-card').scrollIntoView({block:'center'})"); time.sleep(.5); click("Explore graph"); wait_for(".graph-overlay"); shot("05_threat_evidence_graph.png")
                click("Close graph"); click("Runtime"); wait_for(".runtime-layout"); shot("06_runtime_provider.png")
                click("Live Shield"); wait_for(".live-settings"); shot("07_live_shield_opt_in.png")
                click("Privacy"); wait_for(".privacy-hero"); shot("08_privacy.png")
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill()

if __name__=="__main__": main()
