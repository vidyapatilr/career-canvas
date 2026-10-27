"""SQLite storage for the job tracker at data/tracker.db."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tracker.db"
STATUSES = ["Applied", "Interview", "Offer", "Rejected", "Withdrawn"]
COLUMNS = ["id", "company", "position", "date_applied", "pay_range", "status", "notes"]


def _conn(db_path=None):
    path = Path(db_path or DB_PATH)
    path.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            date_applied TEXT,
            pay_range TEXT,
            status TEXT NOT NULL DEFAULT 'Applied',
            notes TEXT
        )"""
    )
    return conn


def list_all(db_path=None):
    with _conn(db_path) as conn:
        rows = conn.execute(
            f"SELECT {', '.join(COLUMNS)} FROM applications ORDER BY date_applied DESC, id DESC"
        ).fetchall()
    return [dict(zip(COLUMNS, r)) for r in rows]


def add(company, position, date_applied, pay_range="", status="Applied", notes="", db_path=None):
    with _conn(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO applications (company, position, date_applied, pay_range, status, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (company, position, date_applied, pay_range, status, notes),
        )
        return cur.lastrowid


def update(row_id, db_path=None, **fields):
    fields = {k: v for k, v in fields.items() if k in COLUMNS and k != "id"}
    if not fields:
        return
    sets = ", ".join(f"{k} = ?" for k in fields)
    with _conn(db_path) as conn:
        conn.execute(f"UPDATE applications SET {sets} WHERE id = ?", (*fields.values(), row_id))


def delete(row_id, db_path=None):
    with _conn(db_path) as conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (row_id,))
