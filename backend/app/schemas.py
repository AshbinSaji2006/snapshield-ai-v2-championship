from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=50_000)
    save_incident: bool = True

    @field_validator("text")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text cannot be blank")
        return value


class URLRequest(BaseModel):
    url: str = Field(min_length=3, max_length=4096)
    save_incident: bool = True


class Signal(BaseModel):
    id: str
    name: str
    severity: Literal["info", "low", "moderate", "high", "critical"]
    description: str
    contribution: float
    evidence: str | None = None
    span: dict[str, int] | None = None


class AnalysisResponse(BaseModel):
    id: str | None = None
    input_type: str
    risk_score: int
    severity: Literal["low", "moderate", "high", "critical"]
    threat_category: str
    classification: str
    confidence: float | None = None
    signals: list[Signal]
    detected_urls: list[str] = []
    pii_findings: list[dict[str, Any]] = []
    redacted_text: str | None = None
    explanation: str
    recommendations: list[str]
    runtime: dict[str, Any]
    processing_time_ms: float
    privacy_status: str = "Processed locally; source content not persisted"
    details: dict[str, Any] = {}
