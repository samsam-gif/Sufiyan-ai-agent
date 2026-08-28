"""
Approval Center Manager for AI Company Command Center.
Tracks approvals requested by agents and owner decisions.
"""
import time
import uuid
from typing import List, Dict, Any, Optional

class ApprovalManager:
    def __init__(self, db):
        self.db = db

    def request_approval(self, project_id: str, agent: str, action: str, risk_level: str, reason: str, task_id: Optional[str] = None) -> str:
        approval_id = f"APP-{uuid.uuid4().hex[:6].upper()}"
        now = time.time()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO approvals (id, project_id, task_id, agent, action, risk_level, reason, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDING', ?)
            """, (approval_id, project_id, task_id, agent, action, risk_level, reason, now))
            conn.commit()
        return approval_id

    def list_approvals(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM approvals WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM approvals ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def resolve_approval(self, approval_id: str, approved: bool, reviewer: str = "owner") -> bool:
        now = time.time()
        new_status = "APPROVED" if approved else "REJECTED"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE approvals
            SET status = ?, reviewed_by = ?, reviewed_at = ?
            WHERE id = ? AND status = 'PENDING'
            """, (new_status, reviewer, now, approval_id))
            affected = cursor.rowcount
            
            # If linked to a task, update task status
            if affected > 0:
                cursor.execute("SELECT task_id FROM approvals WHERE id = ?", (approval_id,))
                row = cursor.fetchone()
                if row and row["task_id"]:
                    next_task_status = "QUEUED" if approved else "CANCELLED"
                    cursor.execute("UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?", (next_task_status, now, row["task_id"]))
            conn.commit()
            return affected > 0
