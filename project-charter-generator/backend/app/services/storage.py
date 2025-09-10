import os
import sqlite3
import json
import datetime
from typing import Dict, Any, List, Optional

DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "database.db"))

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        sponsor TEXT,
        payload_json TEXT,
        result_json TEXT,
        complexity_score REAL,
        recommended_pm_count INTEGER,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def _get_conn():
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def store_submission(payload: Dict[str, Any]) -> int:
    """
    Insert the incoming submission payload (raw JSON).
    Returns the inserted row id.
    """
    conn = _get_conn()
    cur = conn.cursor()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    project_name = payload.get("project_name") if isinstance(payload, dict) else None
    sponsor = payload.get("sponsor") if isinstance(payload, dict) else None
    payload_text = json.dumps(payload, ensure_ascii=False)
    cur.execute(
        "INSERT INTO submissions (project_name, sponsor, payload_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (project_name, sponsor, payload_text, now, now)
    )
    rowid = cur.lastrowid
    conn.commit()
    conn.close()
    return rowid

def save_result(submission_id: int, result: Dict[str, Any]) -> None:
    """
    Save LLM result (a dict) for the given submission id.
    Updates result_json, complexity_score and recommended_pm_count where available.
    """
    conn = _get_conn()
    cur = conn.cursor()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    try:
        result_text = json.dumps(result, ensure_ascii=False)
    except Exception:
        # Fallback to string if serialization fails
        result_text = str(result)

    complexity = None
    pm_count = None
    # try to pick well-known keys from result
    if isinstance(result, dict):
        complexity = result.get("complexity_score") or result.get("complexity") or None
        pm_count = result.get("recommended_pm_count") or result.get("pm_count") or None

    cur.execute(
        "UPDATE submissions SET result_json = ?, complexity_score = ?, recommended_pm_count = ?, updated_at = ? WHERE id = ?",
        (result_text, complexity, pm_count, now, submission_id)
    )
    conn.commit()
    conn.close()

def list_submissions(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Return most recent submissions as list of dicts.
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, project_name, sponsor, payload_json, result_json, complexity_score, recommended_pm_count, created_at, updated_at FROM submissions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        pid = r["id"]
        pname = r["project_name"]
        sponsor = r["sponsor"]
        payload_text = r["payload_json"]
        result_text = r["result_json"]
        created_at = r["created_at"]
        updated_at = r["updated_at"]
        try:
            payload = json.loads(payload_text) if payload_text else None
        except Exception:
            payload = payload_text
        try:
            result = json.loads(result_text) if result_text else None
        except Exception:
            result = result_text
        results.append({
            "id": pid,
            "project_name": pname,
            "sponsor": sponsor,
            "payload": payload,
            "result": result,
            "complexity_score": r["complexity_score"],
            "recommended_pm_count": r["recommended_pm_count"],
            "created_at": created_at,
            "updated_at": updated_at
        })
    return results

def get_submission(submission_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetch a single submission by id.
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, project_name, sponsor, payload_json, result_json, complexity_score, recommended_pm_count, created_at, updated_at FROM submissions WHERE id = ?", (submission_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    try:
        payload = json.loads(row["payload_json"]) if row["payload_json"] else None
    except Exception:
        payload = row["payload_json"]
    try:
        result = json.loads(row["result_json"]) if row["result_json"] else None
    except Exception:
        result = row["result_json"]
    return {
        "id": row["id"],
        "project_name": row["project_name"],
        "sponsor": row["sponsor"],
        "payload": payload,
        "result": result,
        "complexity_score": row["complexity_score"],
        "recommended_pm_count": row["recommended_pm_count"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }
