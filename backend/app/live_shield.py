"""Opt-in clipboard monitor. OFF at every startup; volatile state, no implicit saving."""
from collections import deque
import ctypes
import hashlib
import platform
import threading
import time

def read_clipboard_text():
    if platform.system()!="Windows": return None
    from ctypes import wintypes
    user=ctypes.windll.user32; kernel=ctypes.windll.kernel32
    user.GetClipboardData.argtypes=[wintypes.UINT]; user.GetClipboardData.restype=wintypes.HANDLE
    kernel.GlobalLock.argtypes=[wintypes.HGLOBAL]; kernel.GlobalLock.restype=ctypes.c_void_p
    kernel.GlobalSize.argtypes=[wintypes.HGLOBAL]; kernel.GlobalSize.restype=ctypes.c_size_t
    kernel.GlobalUnlock.argtypes=[wintypes.HGLOBAL]
    if not user.IsClipboardFormatAvailable(13) or not user.OpenClipboard(None): return None
    try:
        handle=user.GetClipboardData(13)
        size=kernel.GlobalSize(handle) if handle else 0
        if not handle or size<2 or size>100002: return None
        pointer=kernel.GlobalLock(handle)
        if not pointer: return None
        try:
            text=ctypes.wstring_at(pointer,size//2).split("\x00",1)[0]
            return text if text.strip() and len(text)<=50000 else None
        finally: kernel.GlobalUnlock(handle)
    finally: user.CloseClipboard()

class LiveShield:
    def __init__(self, analyzer=None, clock=time.monotonic):
        self.enabled=False; self._stop=threading.Event(); self._thread=None
        self._lock=threading.RLock(); self._seen=deque(maxlen=128); self._last=-float("inf")
        self._latest=None; self._generation=0; self.scans=0; self._clock=clock; self._analyzer=analyzer
        self.error=None

    def status(self):
        with self._lock:
            return {"enabled":self.enabled,"available":platform.system()=="Windows","scans":self.scans,"persistence":False,
                    "minimum_interval_seconds":3,"error":self.error,"scope":"Windows text clipboard only while explicitly enabled"}

    def start(self, *, start_thread=True):
        with self._lock:
            if self.enabled: return
            self.enabled=True; self._generation+=1; self._stop.clear(); self.error=None
            if start_thread:
                self._thread=threading.Thread(target=self._loop,name="SnapShieldLive",daemon=True); self._thread.start()

    def stop(self):
        with self._lock:
            self.enabled=False; self._generation+=1; self._stop.set(); self._latest=None; self._seen.clear()
        if self._thread and self._thread is not threading.current_thread(): self._thread.join(timeout=2)

    def process(self,text):
        if not isinstance(text,str) or not text.strip() or len(text)>50000: return None
        digest=hashlib.sha256(text.encode("utf-8",errors="replace")).hexdigest()
        with self._lock:
            now=self._clock()
            if not self.enabled or digest in self._seen or now-self._last<3: return None
            self._last=now; self._seen.append(digest); generation=self._generation
        if self._analyzer is None:
            from .orchestrator import analyze_text_full
            analyzer=analyze_text_full
        else: analyzer=self._analyzer
        result=analyzer(text,False)
        with self._lock:
            # An in-flight result is discarded if the user disables monitoring.
            if not self.enabled or generation!=self._generation: return None
            self.scans+=1
            if result["risk_score"]>=50:
                self._latest={"sequence":self.scans,"created":self._clock(),"result":result,"digest":digest}
                return result
        return None

    def latest(self):
        with self._lock:
            if self._latest and self._clock()-self._latest["created"]>60: self._latest=None
            return None if self._latest is None else {"sequence":self._latest["sequence"],"result":self._latest["result"]}

    def ignore(self):
        with self._lock: self._latest=None

    def save(self):
        from .database import create_incident
        with self._lock:
            if not self.latest(): return None
            item=self._latest
            identifier=create_incident(item["result"],item["digest"])
            self._latest=None
            return identifier

    def _loop(self):
        # Only future clipboard changes after opt-in are considered.
        sequence=ctypes.windll.user32.GetClipboardSequenceNumber() if platform.system()=="Windows" else None
        while not self._stop.wait(.5):
            try:
                if platform.system()!="Windows": return
                current=ctypes.windll.user32.GetClipboardSequenceNumber()
                if current==sequence: continue
                text=read_clipboard_text()
                if text is None: sequence=current; continue
                # Keep latest clipboard change eligible once the rate limit passes.
                if self._clock()-self._last>=3:
                    self.process(text); sequence=current
                text=None
            except Exception as exc:
                with self._lock: self.error=f"Clipboard analysis unavailable ({type(exc).__name__}); manual analysis remains available"

live_shield=LiveShield()
