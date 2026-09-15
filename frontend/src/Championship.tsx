import { useEffect, useState } from 'react'
import { Activity, GitBranch, Maximize2, ShieldCheck, X } from 'lucide-react'
import type { Analysis } from './types'

export type GraphNode = { id: string; type: string; label: string; details: Record<string, unknown> }
export type Graph = { nodes: GraphNode[]; edges: {id:string;source:string;target:string;type:string}[]; description:string }
export type Routing = { path:string; reasons:string[]; deep_executed:boolean; entropy_bits?:number }
export type LiveStatus = {enabled:boolean;available:boolean;scans:number;error?:string}
export type LiveAlert = {sequence:number;result:Analysis}

export function AdaptiveEvidence({ result }: {result:Analysis}) {
  const routing=result.details.routing
  const normalized=result.details.normalization
  if (!routing) return null
  return <section className="card adaptive-card"><div className="section-title"><div><span className="eyebrow">Adaptive local intelligence</span><h3><GitBranch size={17}/> {routing.deep_executed ? 'Deep Guard engaged' : routing.path==='fast_fallback' ? 'Fast Guard · fallback' : 'Fast Guard · fast path'}</h3></div><span className="count">{routing.path.replaceAll('_',' ')}</span></div>
    <ol className="route-reasons">{routing.reasons.map(r=><li key={r}>{r}</li>)}</ol>
    <div className="compute-steps"><span>Fast Guard</span><span>Context router</span><span className={routing.deep_executed?'engaged':''}>{routing.deep_executed?'Deep Guard':'Deep skipped'}</span><span>Evidence fusion</span></div>
    {normalized && normalized.transformations.length>0 && <details className="normalized"><summary>Review {normalized.transformations.length} normalization steps</summary><p>{normalized.transformations.join(' · ')}</p><label>Original evidence · sensitive fields redacted</label><pre>{normalized.original_text_redacted}</pre><label>Normalized security view · sensitive fields redacted</label><pre>{normalized.normalized_security_text_redacted}</pre></details>}
    <small>Risk score is an evidence index. It is not a probability of harm.</small>
  </section>
}

export function EvidenceGraph({ graph }: {graph?:Graph}) {
  const [expanded,setExpanded]=useState(false)
  const [selected,setSelected]=useState<GraphNode>()
  useEffect(()=>{ if(!expanded)return; const escape=(e:KeyboardEvent)=>{if(e.key==='Escape')setExpanded(false)}; document.addEventListener('keydown',escape); return ()=>document.removeEventListener('keydown',escape) },[expanded])
  if(!graph)return null
  const priority=['Input','OCRText','QRPayload','TextEvidence','URL','Domain','ClaimedBrand','ExpectedBrandDomain','MLFinding','RuleFinding','RiskDecision']
  const displayed=graph.nodes.filter(n=>n.type!=='RoutingDecision').sort((a,b)=>priority.indexOf(a.type)-priority.indexOf(b.type))
  const focus=displayed.filter(n=>n.type!=='RuleFinding').concat(displayed.filter(n=>n.type==='RuleFinding').slice(0,3))
  const columns=[focus.filter(n=>['Input','OCRText','QRPayload','TextEvidence'].includes(n.type)),focus.filter(n=>['URL','Domain'].includes(n.type)),focus.filter(n=>['ClaimedBrand','ExpectedBrandDomain'].includes(n.type)),focus.filter(n=>['MLFinding','RuleFinding','RiskDecision'].includes(n.type))]
  const positioned=columns.flatMap((items,column)=>items.slice(0,5).map((n,row)=>({...n,x:column*255+15,y:row*78+30})))
  const positions=new Map(positioned.map(n=>[n.id,n]))
  const chart=<svg className="threat-graph" viewBox="0 0 1040 440" role="img" aria-label="Interactive threat evidence correlation graph"><defs><marker id="arrow-v2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#658579"/></marker></defs>
    {graph.edges.map(e=>{const a=positions.get(e.source),b=positions.get(e.target); if(!a||!b)return null; return <path key={e.id} d={`M${a.x+215},${a.y+26} C${a.x+245},${a.y+26} ${b.x-25},${b.y+26} ${b.x},${b.y+26}`} fill="none" stroke={e.type==='conflicts_with'?'#ff6b73':'#38544a'} strokeWidth={e.type==='conflicts_with'?3:1.5} markerEnd="url(#arrow-v2)"><title>{e.type.replaceAll('_',' ')}</title></path>})}
    {positioned.map(n=><g key={n.id} role="button" tabIndex={0} aria-label={`${n.type}: ${n.label}`} onClick={()=>setSelected(n)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' ')setSelected(n)}} className={`graph-node ${n.type==='RiskDecision'?'verdict':''}`}><rect x={n.x} y={n.y} width="215" height="55" rx="10" fill={selected?.id===n.id?'#203f33':'#101d19'} stroke={n.type==='RiskDecision'?'#ff986b':'#426353'}/><text x={n.x+12} y={n.y+19} fill="#8bbba6" fontSize="11">{n.type.replace(/([a-z])([A-Z])/g,'$1 $2').toUpperCase()}</text><text x={n.x+12} y={n.y+40} fill="#edf8f2" fontSize="14">{n.label.length>25?n.label.slice(0,24)+'…':n.label}</text></g>)}
  </svg>
  const detail=selected?<div className="graph-detail"><strong>{selected.label}</strong><span>{selected.type}</span><p>{String(selected.details.description||selected.details.provenance||'Locally derived evidence relationship')}</p><pre>{JSON.stringify(selected.details,null,2)}</pre><div>{graph.edges.filter(e=>e.source===selected.id||e.target===selected.id).map(e=><p key={e.id}>{graph.nodes.find(n=>n.id===e.source)?.label} → <b>{e.type.replaceAll('_',' ')}</b> → {graph.nodes.find(n=>n.id===e.target)?.label}</p>)}</div></div>:<p className="muted">Select a node to inspect its source, contribution, and relationships. Red edges highlight domain conflicts.</p>
  return <section className="card graph-card"><div className="section-title"><div><span className="eyebrow">Connected security evidence</span><h3>Threat evidence graph</h3></div><button className="ghost-button" onClick={()=>setExpanded(true)}><Maximize2 size={15}/> Explore graph</button></div><p className="muted">{graph.nodes.length} evidence nodes · {graph.edges.length} relationships · locally correlated</p>{chart}{!expanded&&detail}
    {expanded&&<div className="graph-overlay" role="dialog" aria-modal="true" aria-label="Expanded threat evidence graph"><section><div className="section-title"><div><span className="eyebrow">SnapShield AI · evidence correlation</span><h2>Follow the evidence.</h2></div><button className="ghost-button" autoFocus onClick={()=>setExpanded(false)}><X size={20}/> Close graph</button></div>{chart}{detail}<p className="muted">{graph.description}</p></section></div>}
  </section>
}

export async function liveRequest<T>(path:string, body?:unknown):Promise<T> {
  const response=await fetch('/api/live/'+path,body===undefined?undefined:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
  if(!response.ok){const data=await response.json();throw new Error(data.detail||'Local clipboard service unavailable')}
  return response.json()
}

export function LiveShieldView({status,alert,refresh}:{status?:LiveStatus;alert?:LiveAlert;refresh:()=>void}) {
  const [consent,setConsent]=useState(false); const [error,setError]=useState(''); const [show,setShow]=useState(false)
  async function control(enabled:boolean){setError('');try{await liveRequest('control',{enabled,consent});refresh()}catch(e){setError(String(e))}}
  const demo='SBI: Aapka KYC block hone wala hai. Apna OTP bhejo aur verify karo http://sbi-update.example/login immediately.'
  return <main className="content"><div className="page-heading"><div><span className="eyebrow">Optional proactive protection</span><h1>Live Shield</h1><p>Inspect newly copied text locally while you choose to keep protection on.</p></div><span className={`severity ${status?.enabled?'low':'moderate'}`}>{status?.enabled?'Active · clipboard':'Off · no monitoring'}</span></div>
    <section className="card live-settings"><ShieldCheck size={40}/><div><h2>Your clipboard. Your control.</h2><p>Off by default. No keystrokes, browser history, or screen recording. Repeated content is deduplicated; checks run at most once every three seconds. Alerts expire after one minute and are only saved when you choose.</p><label className="consent"><input type="checkbox" checked={consent} onChange={e=>setConsent(e.target.checked)}/> I allow local analysis of new text clipboard changes while Live Shield is enabled.</label><button className="primary" disabled={!status?.enabled&&(!consent||!status?.available)} onClick={()=>control(!status?.enabled)}>{status?.enabled?'Turn off and clear alert':'Enable Live Shield'}</button><button className="ghost-button" onClick={async()=>{try{await navigator.clipboard.writeText(demo)}catch{setError('Clipboard write unavailable. Copy the safe sample manually.')}}}>Copy safe scam demo</button><pre>{demo}</pre><small>{status?.scans??0} local checks this session · no automatic incident storage</small></div></section>
    {(error||status?.error)&&<p role="alert" className="error">{error||status?.error}</p>}
    {alert&&<section className="card live-alert"><Activity/><h2>{alert.result.severity.toUpperCase()} · {alert.result.risk_score}/100</h2><p>{alert.result.signals.filter(s=>s.contribution>0).slice(0,3).map(s=>s.name).join(' · ')}</p><button className="primary" onClick={()=>setShow(!show)}>Open in SnapShield</button><button className="ghost-button" onClick={async()=>{await liveRequest('ignore',{});refresh()}}>Ignore</button><button className="ghost-button" onClick={async()=>{await liveRequest('save',{});refresh()}}>Save sanitized incident</button>{show&&<><AdaptiveEvidence result={alert.result}/><EvidenceGraph graph={alert.result.details.evidence_graph}/><p>{alert.result.explanation}</p></>}</section>}
  </main>
}
