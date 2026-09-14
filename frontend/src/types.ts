export type Signal = { id: string; name: string; severity: string; description: string; contribution: number; evidence?: string }
export type AnalysisDetails = {
  ocr?: { engine: string; available: boolean; text: string; characters: number; line_count: number; confidence: number; processing_time_ms: number };
  qr?: { decoder: string; count: number; contents: string[]; types: string[] };
  [key: string]: unknown;
}
export type Analysis = {
  id?: string; input_type: string; risk_score: number; severity: string; threat_category: string;
  classification: string; confidence?: number; signals: Signal[]; detected_urls: string[];
  pii_findings: { type: string; masked_value: string; confidence: string; risk_note: string }[];
  redacted_text?: string; explanation: string; recommendations: string[];
  runtime: Runtime; processing_time_ms: number; privacy_status: string; details: AnalysisDetails
}
export type Runtime = {
  os: string; architecture: string; python: string; selected_provider: string; available_onnx_providers: string[];
  model_readiness: string; snapdragon_npu_verified: boolean; snapdragon_status: string; cloud_ai_enabled: boolean;
  hardware_acceleration?: string; ocr?: { available: boolean; engine: string; local: boolean };
  model?: { name: string; version: string; provider: string; onnx: boolean; model_file: string }
}
export type Incident = {
  id: string; created_at: string; input_type: string; threat_score: number; severity: string; threat_category: string;
  classification: string; indicator_count: number; processing_time_ms: number; runtime_provider: string; sanitized_summary: string;
  model_version: string; evidence: { id: string; name: string; severity: string }[]
}
