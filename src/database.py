# src/database.py
import sqlite3
import time
from typing import List, Tuple, Dict, Any

DB_FILE = "governance_engine.db"

def initialize_database() -> None:
    """
    Executes raw DDL statement blocks to initialize third-normal-form (3NF) relational tables.
    """
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # Enable foreign key verification enforcement
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Core enterprise ticket data store
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                severity INTEGER NOT NULL,
                sla_hours INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
        """)
        
        # Audit logs to preserve complete operational history tracing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                previous_status TEXT NOT NULL,
                new_status TEXT NOT NULL,
                changed_at REAL NOT NULL,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
            );
        """)
        conn.commit()

def create_ticket(category: str, description: str, severity: int, sla_hours: int) -> int:
    """
    Performs data injection using safe parameterized execution queries.
    """
    current_time = time.time()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO tickets (category, description, severity, sla_hours, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, 'Open', ?, ?);""",
            (category, description, severity, sla_hours, current_time, current_time)
        )
        conn.commit()
        return cursor.lastrowid

def fetch_active_tickets() -> List[Dict[str, Any]]:
    """
    Fetches unresolved governance items for scheduling load.
    """
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE status != 'Resolved';")
        return [dict(row) for row in cursor.fetchall()]

def transition_ticket_status(ticket_id: int, current_status: str, next_status: str) -> None:
    """
    Executes ACID status modification updates and records state transactions in the audit logs.
    """
    current_time = time.time()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # Update main ticket data
        cursor.execute(
            "UPDATE tickets SET status = ?, updated_at = ? WHERE ticket_id = ?;",
            (next_status, current_time, ticket_id)
        )
        
        # Create audit entry tracing state transition pathways
        cursor.execute(
            "INSERT INTO audit_logs (ticket_id, previous_status, new_status, changed_at) VALUES (?, ?, ?, ?);",
            (ticket_id, current_status, next_status, current_time)
        )
        conn.commit()

def fetch_historical_logs() -> List[Tuple[int, str, str, float]]:
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ticket_id, previous_status, new_status, changed_at FROM audit_logs ORDER BY changed_at DESC;")
        return cursor.fetchall()