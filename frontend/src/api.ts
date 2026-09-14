import type { Analysis, Incident, Runtime } from './types'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options)
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try { const body = await response.json(); message = body.detail || message } catch { /* safe fallback */ }
    throw new Error(message)
  }
  return response.json()
}

export const api = {
  health: () => request<{ status: string; version: string; runtime_provider: string }>('/api/health'),
  runtime: () => request<Runtime>('/api/runtime'),
  text: (text: string) => request<Analysis>('/api/analyze/text', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text }) }),
  url: (url: string) => request<Analysis>('/api/analyze/url', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url }) }),
  image: (file: File) => { const data = new FormData(); data.append('file', file); return request<Analysis>('/api/analyze/image', { method: 'POST', body: data }) },
  demoAsset: async (name: 'demo_screenshot.png' | 'demo_multimodal.png' | 'demo_qr.png') => {
    const response = await fetch(`/api/demo/assets/${name}`); if (!response.ok) throw new Error('Demo asset unavailable')
    return new File([await response.blob()], name, { type: 'image/png' })
  },
  incidents: () => request<Incident[]>('/api/incidents'),
  removeIncident: (id: string) => request<{ deleted: boolean }>(`/api/incidents/${id}`, { method: 'DELETE' }),
  clear: () => request<{ deleted: number }>('/api/incidents', { method: 'DELETE' }),
  stats: () => request<{ total_scans: number; average_risk: number; by_severity: Record<string, number>; top_categories: {name: string; count: number}[] }>('/api/stats'),
  benchmark: () => request<Record<string, string | number | boolean>>('/api/benchmark?iterations=25', { method: 'POST' }),
}
