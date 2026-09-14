import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from typing import Any

from .config import DATA_DIR, DB_PATH

_lock = threading.Lock()


def connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=5)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY, created_at TEXT NOT NULL, input_type TEXT NOT NULL,
                input_hash TEXT NOT NULL, threat_score INTEGER NOT NULL, severity TEXT NOT NULL,
                threat_category TEXT NOT NULL, classification TEXT NOT NULL DEFAULT 'unknown', indicator_count INTEGER NOT NULL,
                processing_time_ms REAL NOT NULL, runtime_provider TEXT NOT NULL,
                sanitized_summary TEXT NOT NULL, model_version TEXT NOT NULL, evidence_json TEXT NOT NULL
            )
        """)
        columns = {row[1] for row in db.execute("PRAGMA table_info(incidents)")}
        if "classification" not in columns:
            db.execute("ALTER TABLE incidents ADD COLUMN classification TEXT NOT NULL DEFAULT 'unknown'")


def create_incident(result: dict[str, Any], input_hash: str) -> str:
    incident_id = str(uuid.uuid4())
    safe_evidence = [{"id": s["id"], "name": s["name"], "severity": s["severity"]} for s in result["signals"]]
    summary = f'{result["severity"].upper()} {result["threat_category"]}; {len(safe_evidence)} indicators'
    model_details = result.get("details", {}).get("model", {})
    model_version = model_details.get("version", "url-rules-v1") if isinstance(model_details, dict) else "unknown"
    values = (
        incident_id, datetime.now(timezone.utc).isoformat(), result["input_type"], input_hash,
        result["risk_score"], result["severity"], result["threat_category"], result["classification"], len(safe_evidence),
        result["processing_time_ms"], result["runtime"]["selected_provider"], summary,
        model_version, json.dumps(safe_evidence),
    )
    with _lock, connect() as db:
        db.execute("""INSERT INTO incidents (
            id, created_at, input_type, input_hash, threat_score, severity,
            threat_category, classification, indicator_count, processing_time_ms,
            runtime_provider, sanitized_summary, model_version, evidence_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", values)
    return incident_id


def list_incidents(limit: int = 100) -> list[dict[str, Any]]:
    with connect() as db:
        rows = db.execute("SELECT * FROM incidents ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return [dict(row) | {"evidence": json.loads(row["evidence_json"])} for row in rows]


def get_incident(incident_id: str) -> dict[str, Any] | None:
    with connect() as db:
        row = db.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    return None if row is None else dict(row) | {"evidence": json.loads(row["evidence_json"])}


def delete_incident(incident_id: str) -> bool:
    with _lock, connect() as db:
        cursor = db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    return cursor.rowcount > 0


def clear_incidents() -> int:
    with _lock, connect() as db:
        count = db.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
        db.execute("DELETE FROM incidents")
    return count


def stats() -> dict[str, Any]:
    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
        avg = db.execute("SELECT COALESCE(AVG(threat_score), 0) FROM incidents").fetchone()[0]
        severity = {row[0]: row[1] for row in db.execute("SELECT severity, COUNT(*) FROM incidents GROUP BY severity")}
        categories = [{"name": row[0], "count": row[1]} for row in db.execute("SELECT threat_category, COUNT(*) FROM incidents GROUP BY threat_category ORDER BY COUNT(*) DESC")]
    return {"total_scans": total, "average_risk": round(avg, 1), "by_severity": severity, "top_categories": categories}
