# src/workflow.py
import pandas as pd
import sqlite3
from typing import Dict, List, Any
from src.database import DB_FILE, transition_ticket_status

VALID_TRANSITIONS: Dict[str, str] = {
    "Open": "Investigating",
    "Investigating": "Escalated",
    "Escalated": "Resolved"
}

class CorporateWorkflowEngine:
    """
    Models business logic constraints by governing allowed operational state changes.
    """
    @staticmethod
    def process_transition(ticket_id: int, current_status: str) -> str:
        """
        Evaluates state paths. A ticket cannot skip intermediate investigation milestones.
        """
        if current_status not in VALID_TRANSITIONS:
            raise ValueError(f"State '{current_status}' cannot be transitioned further.")
        
        next_status = VALID_TRANSITIONS[current_status]
        transition_ticket_status(ticket_id, current_status, next_status)
        return next_status

    @staticmethod
    def generate_kpi_dashboard_metrics() -> Dict[str, Any]:
        """
        Aggregates operational infrastructure metrics into summary metrics.
        """
        with sqlite3.connect(DB_FILE) as conn:
            df_tickets = pd.read_sql_query("SELECT * FROM tickets;", conn)
            
        if df_tickets.empty:
            return {"total": 0, "status_counts": pd.DataFrame(), "severity_avg": 0.0}

        metrics = {
            "total": len(df_tickets),
            "status_counts": df_tickets["status"].value_counts().reset_index(),
            "severity_avg": float(df_tickets["severity"].mean())
        }
        metrics["status_counts"].columns = ["Operational Status", "Volume Totals"]
        return metrics