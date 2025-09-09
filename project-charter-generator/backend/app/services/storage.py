# backend/app/services/storage.py
import os
import sqlite3
import json
import datetime
from typing import Dict, Any, List

DB_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo.db"))

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        sponsor TEXT,
        payload_json TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def store_submission(payload: Dict[str, Any]) -> int:
    """
    Store the incoming submission payload (the whole JSON).
    Returns the inserted row id.
    """
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    project_name = payload.get("project_name") if isinstance(payload, dict) else None
    sponsor = payload.get("sponsor") if isinstance(payload, dict) else None
    payload_text = json.dumps(payload, ensure_ascii=False)
    cur.execute(
        "INSERT INTO submissions (project_name, sponsor, payload_json, created_at) VALUES (?, ?, ?, ?)",
        (project_name, sponsor, payload_text, now)
    )
    rowid = cur.lastrowid
    conn.commit()
    conn.close()
    return rowid

def list_submissions(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Return most recent submissions as list of dicts.
    """
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, project_name, sponsor, payload_json, created_at FROM submissions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        pid, pname, sponsor, payload_text, created_at = r
        try:
            payload = json.loads(payload_text)
        except Exception:
            payload = payload_text
        results.append({
            "id": pid,
            "project_name": pname,
            "sponsor": sponsor,
            "payload": payload,
            "created_at": created_at
        })
    return results
