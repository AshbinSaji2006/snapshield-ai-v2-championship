import { useEffect, useRef, useState } from 'react'
import { Activity, AlertTriangle, BarChart3, Check, ChevronRight, CircleGauge, Clock3, Database, Eye, EyeOff, FileImage, Fingerprint, Gauge, History, Home, Info, KeyRound, Link2, LoaderCircle, LockKeyhole, Menu, Presentation, Radar, RotateCcw, ScanLine, Shield, ShieldAlert, ShieldCheck, Sparkles, Trash2, Upload, WifiOff, X } from 'lucide-react'
import { api } from './api'
import type { Analysis, Incident, Runtime } from './types'
import { AdaptiveEvidence, EvidenceGraph, LiveShieldView, liveRequest } from './Championship'
import type { LiveAlert, LiveStatus } from './Championship'

type View = 'overview' | 'analyze' | 'live' | 'incidents' | 'runtime' | 'privacy' | 'about'
type Mode = 'text' | 'url' | 'image'
const demo = `SECURITY ALERT: Your bank account has been temporarily suspended. Verify your password and OTP immediately at http://paypa1-secure.example/login to avoid closure.`
const demoTexts = [
  { label: 'Legitimate', mode: 'text' as const, value: 'Hi Priya, the university design review is confirmed for Tuesday at 2 PM in Lab 4. No action is needed before the meeting.' },
  { label: 'Bank phish', mode: 'text' as const, value: 'SBI SECURITY ALERT: Your account has been suspended. Verify your password and OTP immediately at http://192.0.2.1:8080/sbi/verify/login.exe' },
  { label: 'Obfuscated', mode: 'text' as const, value: 'Your parcel is held. Pay the fee now at hxxp://delivery-update[.]example/pay.' },
  { label: 'Hinglish', mode: 'text' as const, value: 'SBI KYC block hone wala hai. OTP kisi ko mat batana; official app mein status check karein.' },
  { label: 'PII guard', mode: 'text' as const, value: 'Contact priya@example.com. Example card 4111 1111 1111 1111. password=not-a-real-secret' },
]

function ScoreRing({ score }: { score: number }) {
  const color = score >= 75 ? '#ff5d67' : score >= 50 ? '#ff985b' : score >= 25 ? '#f6c453' : '#56d8a8'
  return <div className="score-ring" style={{ background: `conic-gradient(${color} ${score * 3.6}deg, #20282d 0)` }}>
    <div><strong>{score}</strong><span>/100</span></div>
  </div>
}

function Severity({ value }: { value: string }) { return <span className={`severity ${value}`}><span className="severity-dot" />{value}</span> }

function Header({ runtime, backendOk, onMenu, presentation, onPresentation }: { runtime?: Runtime; backendOk: boolean; onMenu: () => void; presentation: boolean; onPresentation: () => void }) {
  return <header>
    <button className="icon-button mobile-menu" onClick={onMenu} aria-label="Open navigation"><Menu size={20} /></button>
    <div className="top-status"><span className={`status-dot ${backendOk ? '' : 'offline'}`} /> Local AI <strong>{backendOk ? 'active' : 'offline'}</strong></div>
    <div className="header-spacer" />
    <button className={`presentation-toggle ${presentation ? 'active' : ''}`} onClick={onPresentation} aria-pressed={presentation}><Presentation size={15}/>{presentation ? 'Exit presentation' : 'Presentation mode'}</button>
    <div className="provider"><span>AI runtime</span><strong>{runtime?.selected_provider ?? 'Detecting…'}</strong></div>
    <div className="privacy-chip"><LockKeyhole size={14} /> Local processing</div>
  </header>
}

function Sidebar({ view, setView, open, close }: { view: View; setView: (v: View) => void; open: boolean; close: () => void }) {
  const links: [View, typeof Home, string][] = [['overview', Home, 'Command center'], ['analyze', ScanLine, 'Analyze'], ['live', Activity, 'Live Shield'], ['incidents', History, 'Incident center'], ['runtime', Gauge, 'Runtime'], ['privacy', Fingerprint, 'Privacy'], ['about', Info, 'About']]
  return <><aside className={open ? 'open' : ''}>
    <div className="brand"><div className="logo"><Shield size={25} /></div><div><strong>SnapShield</strong><span>AI</span></div><button onClick={close} aria-label="Close navigation"><X /></button></div>
    <div className="product-label">Cyber defense console</div>
    <nav>{links.map(([id, Icon, label]) => <button key={id} className={view === id ? 'active' : ''} onClick={() => { setView(id); close() }}><Icon size={18} /><span>{label}</span>{view === id && <ChevronRight size={15} />}</button>)}</nav>
    <div className="sidebar-foot"><div className="shield-mini"><ShieldCheck size={18} /></div><div><strong>Private by design</strong><span>No cloud AI required</span></div></div>
  </aside>{open && <button className="scrim" onClick={close} aria-label="Close navigation" />}</>
}

function EmptyVisual() {
  return <div className="empty-visual"><div className="radar"><div className="radar-line"/><ShieldCheck size={52}/></div><h3>Ready to inspect</h3><p>Paste a message, URL, or upload a screenshot. Analysis happens through the local pipeline.</p><div className="trust-row"><span><WifiOff size={15}/> No network lookup</span><span><LockKeyhole size={15}/> No source storage</span></div></div>
}

function ResultPanel({ result }: { result: Analysis }) {
  const [redacted, setRedacted] = useState(true)
  const ocr = result.details.ocr
  const qr = result.details.qr
  return <div className="result-stack">
    <section className="result-hero card"><div><div className="eyebrow">Assessment complete</div><h2>{result.threat_category}</h2><div className="result-meta"><Severity value={result.severity}/><span><Clock3 size={14}/>{result.processing_time_ms} ms</span><span><Activity size={14}/>{result.runtime.selected_provider}</span></div></div><ScoreRing score={result.risk_score}/></section>
    <section className="card explanation"><div className="section-icon warning"><Sparkles size={18}/></div><div><h3>Why this was flagged</h3><p>{result.explanation}</p></div></section>
    <AdaptiveEvidence result={result}/>
    {result.input_type === 'image' && (ocr?.available || qr?.count) && <section className="card extraction-card"><div className="section-title"><div><span className="eyebrow">Local image analysis</span><h3>Multimodal extraction</h3></div><span className="local-only"><WifiOff size={13}/> Never opened</span></div>
      <div className="extraction-grid">
        {ocr?.available && <div className="extraction-block"><div className="extraction-label"><FileImage size={15}/><strong>OCR-extracted text</strong><span>{ocr.line_count} lines · {Math.round(ocr.confidence * 100)}% confidence</span></div><pre>{result.redacted_text || 'Text extracted locally.'}</pre></div>}
        {!!qr?.count && <div className="extraction-block"><div className="extraction-label"><Radar size={15}/><strong>QR decoded locally</strong><span>{qr.count} payload{qr.count === 1 ? '' : 's'}</span></div>{qr.contents.map((content, index) => <code key={`${content}-${index}`}>{content}</code>)}</div>}
      </div>
      {!!result.detected_urls.length && <div className="detected-destinations"><span>Detected destination{result.detected_urls.length === 1 ? '' : 's'}</span>{result.detected_urls.map(url => <code key={url}>{url}</code>)}</div>}
    </section>}
    <EvidenceGraph graph={result.details.evidence_graph}/>
    <section className="card"><div className="section-title"><div><span className="eyebrow">Evidence trail</span><h3>Detected indicators</h3></div><span className="count">{result.signals.length}</span></div>
      <div className="signals">{result.signals.length ? result.signals.map(signal => <article className="signal" key={`${signal.id}-${signal.evidence}`}><div className={`signal-icon ${signal.severity}`}>{signal.severity === 'info' ? <Check size={17}/> : <AlertTriangle size={17}/>}</div><div><div className="signal-head"><strong>{signal.name}</strong><span>+{signal.contribution}</span></div><p>{signal.description}</p>{signal.evidence && <code>{signal.evidence}</code>}</div></article>) : <div className="no-signals"><ShieldCheck size={24}/><span>No strong indicators detected</span></div>}</div>
    </section>
    {result.pii_findings.length > 0 && <section className="card"><div className="section-title"><div><span className="eyebrow">Privacy guard</span><h3>Sensitive data</h3></div><button className="text-button" onClick={() => setRedacted(!redacted)}>{redacted ? <Eye size={16}/> : <EyeOff size={16}/>} {redacted ? 'Show original' : 'Show redacted'}</button></div>
      <div className="redacted-block">{redacted ? result.redacted_text : 'Original is intentionally kept only in your active browser session.'}</div>
      <div className="pii-tags">{result.pii_findings.map((p, i) => <span key={i}><KeyRound size={13}/>{p.type}: {p.masked_value}</span>)}</div></section>}
    <section className="card action-card"><div className="section-icon safe"><ShieldCheck size={18}/></div><div><h3>Recommended action</h3><ol>{result.recommendations.map((item, i) => <li key={i}>{item}</li>)}</ol></div></section>
    <div className="privacy-line"><LockKeyhole size={14}/>{result.privacy_status}</div>
  </div>
}

function Analyze({ initialDemo = false }: { initialDemo?: boolean }) {
  const [mode, setMode] = useState<Mode>('text'); const [value, setValue] = useState(initialDemo ? demo : ''); const [file, setFile] = useState<File>(); const [result, setResult] = useState<Analysis>(); const [loading, setLoading] = useState(false); const [error, setError] = useState(''); const inputRef = useRef<HTMLInputElement>(null)
  const reset = () => { setMode('text'); setValue(''); setFile(undefined); setResult(undefined); setError('') }
  const loadImageDemo = async (name: 'demo_multimodal.png' | 'demo_qr.png') => { setError(''); try { setFile(await api.demoAsset(name)); setMode('image'); setResult(undefined) } catch (e) { setError(e instanceof Error ? e.message : 'Demo unavailable') } }
  const run = async () => {
    setError(''); setLoading(true); setResult(undefined)
    try { setResult(mode === 'text' ? await api.text(value) : mode === 'url' ? await api.url(value) : file ? await api.image(file) : (() => { throw new Error('Choose an image first') })()) } catch (e) { setError(e instanceof Error ? e.message : 'Analysis failed') } finally { setLoading(false) }
  }
  return <main className="content analyze-page"><div className="page-heading"><div><span className="eyebrow">Local threat lab</span><h1>Analyze suspicious content</h1><p>Every engine runs locally. Links are parsed, never opened.</p></div><div className="heading-actions"><button className="ghost-button" onClick={() => { setMode('text'); setValue(demo); setResult(undefined) }}><Sparkles size={16}/> Bank demo</button><button className="ghost-button" onClick={reset}><RotateCcw size={16}/> Reset</button></div></div>
    <div className="workspace"><section className="composer card"><div className="mode-tabs" role="tablist"><button className={mode === 'text' ? 'active' : ''} onClick={() => setMode('text')}><Radar size={16}/>Message</button><button className={mode === 'url' ? 'active' : ''} onClick={() => setMode('url')}><Link2 size={16}/>URL</button><button className={mode === 'image' ? 'active' : ''} onClick={() => setMode('image')}><FileImage size={16}/>Image</button></div>
      <div className="demo-strip" aria-label="Safe demo samples"><span>Demos</span>{demoTexts.map(sample => <button key={sample.label} onClick={() => { setMode(sample.mode); setValue(sample.value); setFile(undefined); setResult(undefined) }}>{sample.label}</button>)}<button onClick={() => loadImageDemo('demo_multimodal.png')}>Screenshot</button><button onClick={() => loadImageDemo('demo_qr.png')}>QR</button></div>
      {mode !== 'image' ? <div className="input-wrap"><label htmlFor="analysis-input">{mode === 'text' ? 'Message or email content' : 'Suspicious URL'}</label>{mode === 'text' ? <textarea id="analysis-input" value={value} onChange={e => setValue(e.target.value)} placeholder="Paste suspicious text here…" maxLength={50000}/> : <input id="analysis-input" type="text" value={value} onChange={e => setValue(e.target.value)} placeholder="https://example.com/verify"/>}<span className="char-count">{value.length.toLocaleString()} / {mode === 'text' ? '50,000' : '4,096'}</span></div> : <button className="dropzone" onClick={() => inputRef.current?.click()}><Upload size={28}/><strong>{file ? file.name : 'Choose an image to inspect'}</strong><span>PNG, JPEG, or WEBP · up to 10 MB</span><input ref={inputRef} hidden type="file" accept="image/png,image/jpeg,image/webp" onChange={e => setFile(e.target.files?.[0])}/></button>}
      {error && <div className="error"><AlertTriangle size={16}/>{error}</div>}
      <div className="composer-foot"><span><LockKeyhole size={14}/> Input stays in process memory</span><button className="primary" disabled={loading || (mode !== 'image' ? !value.trim() : !file)} onClick={run}>{loading ? <LoaderCircle className="spin" size={18}/> : <ScanLine size={18}/>} {loading ? 'Analyzing…' : 'Analyze locally'}</button></div></section>
      <section className="results-area">{result ? <ResultPanel result={result}/> : <EmptyVisual/>}</section></div></main>
}

function Overview({ stats, goAnalyze }: { stats?: {total_scans:number;average_risk:number;by_severity:Record<string,number>}; goAnalyze: () => void }) {
  return <main className="content"><div className="hero-copy"><span className="eyebrow">Private on-device cyber defense</span><h1>Your data never needs to leave your device <em>to protect your device.</em></h1><p>Inspect messages, links, and screenshots with independent security engines fused into one explainable risk assessment.</p><button className="primary large" onClick={goAnalyze}><ScanLine size={19}/> Start local analysis</button></div>
    <div className="guard-status"><span><b>FAST GUARD</b> · ACTIVE</span><span><b>DEEP GUARD</b> · ADAPTIVE</span><span><b>EVIDENCE GRAPH</b> · LOCAL</span><span><b>LIVE SHIELD</b> · OPT-IN</span></div>
    <div className="stat-grid"><div className="stat-card"><div className="stat-icon mint"><ShieldCheck/></div><span>Local scans</span><strong>{stats?.total_scans ?? '—'}</strong><small>Sanitized records only</small></div><div className="stat-card"><div className="stat-icon amber"><CircleGauge/></div><span>Average risk</span><strong>{stats?.average_risk ?? '—'}</strong><small>Across recorded incidents</small></div><div className="stat-card"><div className="stat-icon coral"><ShieldAlert/></div><span>High + critical</span><strong>{(stats?.by_severity?.high ?? 0) + (stats?.by_severity?.critical ?? 0)}</strong><small>Needs attention</small></div></div>
    <section className="engines"><div className="page-heading compact"><div><span className="eyebrow">Defense in depth</span><h2>One input. Multiple independent engines.</h2></div></div><div className="engine-grid">{[[Radar,'Language intelligence','Local ML + social engineering rules'],[Link2,'URL forensics','Structural analysis without navigation'],[Fingerprint,'Privacy guard','PII detection and safe redaction'],[BarChart3,'Risk fusion','Transparent evidence-weighted score']].map(([Icon,title,desc]) => { const I=Icon as typeof Radar; return <div className="engine" key={String(title)}><I size={22}/><strong>{String(title)}</strong><p>{String(desc)}</p></div>})}</div></section>
  </main>
}

function IncidentsView({ items, refresh }: { items: Incident[]; refresh: () => void }) {
  const [selected, setSelected] = useState<Incident>()
  const remove = async (id: string) => { await api.removeIncident(id); refresh() }
  const clear = async () => { if (confirm('Delete all sanitized incident records?')) { await api.clear(); refresh() } }
  return <main className="content"><div className="page-heading"><div><span className="eyebrow">Local history</span><h1>Incident center</h1><p>Only hashes, scores, and sanitized evidence metadata are retained.</p></div>{items.length > 0 && <button className="danger-button" onClick={clear}><Trash2 size={16}/> Clear history</button>}</div>
    <div className="incident-layout"><div className="table-card card">{items.length ? <div className="incident-list">{items.map(i => <article key={i.id} className={selected?.id === i.id ? 'selected' : ''}><div className={`incident-mark ${i.severity}`}><ShieldAlert size={18}/></div><button className="incident-main" onClick={() => setSelected(i)}><div><strong>{i.threat_category}</strong><Severity value={i.severity}/></div><span>{new Date(i.created_at).toLocaleString()} · {i.input_type} · {i.indicator_count} indicators</span></button><div className="incident-score">{i.threat_score}<small>/100</small></div><button className="icon-button" onClick={() => remove(i.id)} aria-label="Delete incident"><Trash2 size={16}/></button></article>)}</div> : <div className="empty-list"><Database size={34}/><h3>No incidents yet</h3><p>Completed analyses will appear here as privacy-safe records.</p></div>}</div>
    {selected && <section className="incident-detail card"><button className="detail-close" onClick={() => setSelected(undefined)} aria-label="Close incident detail"><X size={17}/></button><span className="eyebrow">Sanitized forensic record</span><h2>{selected.threat_category}</h2><div className="detail-score"><strong>{selected.threat_score}</strong><Severity value={selected.severity}/></div><dl><div><dt>Timestamp</dt><dd>{new Date(selected.created_at).toLocaleString()}</dd></div><div><dt>Input type</dt><dd>{selected.input_type}</dd></div><div><dt>Classification</dt><dd>{selected.classification}</dd></div><div><dt>Runtime</dt><dd>{selected.runtime_provider}</dd></div><div><dt>Latency</dt><dd>{selected.processing_time_ms} ms</dd></div><div><dt>Model</dt><dd>{selected.model_version}</dd></div></dl><h3>Sanitized evidence</h3><div className="detail-evidence">{selected.evidence.map(item => <span key={item.id}>{item.name}</span>)}</div><p>No source message, URL, image, secret, or extracted PII is stored.</p></section>}</div></main>
}

function RuntimeView({ runtime }: { runtime?: Runtime }) {
  const [bench, setBench] = useState<Record<string,string|number|boolean>>(); const [running,setRunning]=useState(false)
  const run = async () => { setRunning(true); try { setBench(await api.benchmark()) } finally { setRunning(false) } }
  return <main className="content"><div className="page-heading"><div><span className="eyebrow">Hardware-aware inference</span><h1>Runtime</h1><p>Live capability detection. Unverified accelerators are never claimed.</p></div></div>
    <div className="guard-status"><span><b>Fast Guard</b> · ACTIVE</span><span><b>Deep Guard</b> · {runtime?.deep_guard?.ready?'ACTIVE':'FALLBACK'}</span><span><b>Adaptive routing</b> · ACTIVE</span><span><b>QNN / NPU</b> · {runtime?.snapdragon_npu_verified?'VERIFIED':'VALIDATION PENDING'}</span></div>
    <div className="runtime-layout"><section className="card runtime-primary"><div className="runtime-orb"><Activity size={30}/></div><div><span className="eyebrow">Selected provider</span><h2>{runtime?.selected_provider ?? 'Detecting…'}</h2><p>{runtime?.snapdragon_npu_verified ? 'Snapdragon QNN execution provider detected and verified.' : 'CPU fallback is active. The QNN path is ready for validation on compatible Snapdragon hardware.'}</p></div><span className="live"><span/>Live</span></section>
      <section className="card spec-list">{[['Operating system',runtime?.os],['Architecture',runtime?.architecture],['Execution provider',runtime?.selected_provider],['Hardware acceleration',runtime?.hardware_acceleration],['Deployable model',runtime?.model?.model_file],['ONNX model',runtime?.model?.onnx ? `Active · v${runtime.model.version}` : 'Fallback'],['Local OCR',runtime?.ocr?.available ? runtime.ocr.engine : 'Unavailable'],['Cloud AI',runtime?.cloud_ai_enabled ? 'Enabled' : 'Disabled'],['Snapdragon NPU',runtime?.snapdragon_npu_verified ? 'Verified' : 'Awaiting hardware validation']].map(([k,v])=><div key={k}><span>{k}</span><strong>{v ?? '—'}</strong></div>)}</section>
      <section className="card benchmark"><div className="section-title"><div><span className="eyebrow">Measured here</span><h3>Local pipeline benchmark</h3></div><button className="ghost-button" onClick={run} disabled={running}>{running?<LoaderCircle className="spin" size={16}/>:<Gauge size={16}/>} Run</button></div>{bench ? <div className="bench-grid"><div><span>Median</span><strong>{bench.median_ms} ms</strong></div><div><span>P95</span><strong>{bench.p95_ms} ms</strong></div><div><span>Iterations</span><strong>{bench.iterations}</strong></div></div> : <p className="muted">Run 25 real analyses on this machine. Results are not presented as Snapdragon measurements.</p>}</section>
    </div></main>
}

function Privacy() { return <main className="content"><div className="page-heading"><div><span className="eyebrow">Your content, your boundary</span><h1>Privacy architecture</h1><p>Protection without turning sensitive evidence into somebody else’s data.</p></div></div><div className="privacy-hero card"><LockKeyhole size={42}/><div><h2>Local-first by construction</h2><p>Messages, URLs, and images are analyzed by the local API. There is no cloud AI integration and suspicious URLs are never visited.</p></div></div><div className="policy-grid">{[['What enters','Only content you explicitly submit for analysis.'],['What persists','A SHA-256 input hash, score, category, timing, and sanitized indicator names.'],['What does not persist','Raw messages, images, full URLs, passwords, tokens, and extracted PII.'],['Your control','Delete one incident or clear the entire local history at any time.']].map(([a,b])=><article className="card" key={a}><ShieldCheck size={20}/><h3>{a}</h3><p>{b}</p></article>)}</div></main> }

function About() { return <main className="content"><div className="about card"><div className="logo big"><Shield size={42}/></div><span className="eyebrow">Version 2.0 Championship Build</span><h1>SnapShield AI</h1><p className="lead">Adaptive, Private On-Device Multimodal Cyber Defense for Snapdragon PCs.</p><div className="about-note"><Info size={18}/><p>Designed for Snapdragon NPU acceleration. NPU execution is reported only when a QNN provider is actually verified; CPU remains the dependable fallback.</p></div><span className="license">MIT licensed · Built for the Snapdragon® AI Lab Build &amp; Present Challenge</span></div></main> }

export default function App() {
  const [view,setView]=useState<View>('overview'); const [runtime,setRuntime]=useState<Runtime>(); const [stats,setStats]=useState<{total_scans:number;average_risk:number;by_severity:Record<string,number>}>(); const [incidents,setIncidents]=useState<Incident[]>([]); const [ok,setOk]=useState(false); const [menu,setMenu]=useState(false); const [presentation,setPresentation]=useState(false); const [liveStatus,setLiveStatus]=useState<LiveStatus>(); const [liveAlert,setLiveAlert]=useState<LiveAlert>()
  const refresh = () => { api.incidents().then(setIncidents).catch(()=>{}); api.stats().then(setStats).catch(()=>{}) }
  const refreshLive = () => { liveRequest<LiveStatus>('status').then(setLiveStatus).catch(()=>{}); liveRequest<LiveAlert|undefined>('latest').then(setLiveAlert).catch(()=>{}) }
  useEffect(()=>{ api.health().then(()=>setOk(true)).catch(()=>setOk(false)); api.runtime().then(setRuntime).catch(()=>{}); refresh(); refreshLive(); const poll=window.setInterval(refreshLive,1500); return()=>window.clearInterval(poll) },[])
  useEffect(()=>{ if(view==='incidents'||view==='overview') refresh() },[view])
  return <div className={`app ${presentation ? 'presentation' : ''}`}><Sidebar view={view} setView={setView} open={menu} close={()=>setMenu(false)}/><div className="shell"><Header runtime={runtime} backendOk={ok} onMenu={()=>setMenu(true)} presentation={presentation} onPresentation={()=>setPresentation(!presentation)}/>{view==='overview'&&<Overview stats={stats} goAnalyze={()=>setView('analyze')}/>} {view==='analyze'&&<Analyze/>}{view==='live'&&<LiveShieldView status={liveStatus} alert={liveAlert} refresh={()=>{refreshLive();refresh()}}/>}{view==='incidents'&&<IncidentsView items={incidents} refresh={refresh}/>} {view==='runtime'&&<RuntimeView runtime={runtime}/>} {view==='privacy'&&<Privacy/>}{view==='about'&&<About/>}</div>{liveAlert&&view!=='live'&&<div className="live-toast" role="status"><strong>Live Shield · {liveAlert.result.severity.toUpperCase()} {liveAlert.result.risk_score}/100</strong><p>{liveAlert.result.signals.filter(s=>s.contribution>0).slice(0,2).map(s=>s.name).join(' · ')}</p><button onClick={()=>setView('live')}>Open in SnapShield →</button></div>}</div>
}
