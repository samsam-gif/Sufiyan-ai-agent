"""
Structured Audit Logging & Memory Management.
Never records passwords or private API keys.
"""
import time
import re
from typing import List, Dict, Any, Optional

class AuditService:
    def __init__(self, db):
        self.db = db

    def log_action(self, agent: str, action: str, risk_level: str, command: Optional[str], status: str):
        # Sanitize sensitive keywords
        clean_command = self._sanitize(command) if command else None
        now = time.time()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO audit_logs (agent, action, risk_level, command, status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (agent, action, risk_level, clean_command, status, now))
            conn.commit()

    def get_audit_trail(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

    def _sanitize(self, text: str) -> str:
        # Mask api keys and passwords
        masked = re.sub(r'(key|token|password|secret|auth)\s*[:=]\s*([^\s,;]+)', r'\1=***REDACTED***', text, flags=re.IGNORECASE)
        return masked

class MemoryStore:
    def __init__(self, db):
        self.db = db

    def store_memory(self, project_id: str, category: str, key: str, value: str, agent: str):
        now = time.time()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO memory (project_id, category, key, value, agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (project_id, category, key, value, agent, now))
            conn.commit()

    def get_project_memories(self, project_id: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT * FROM memory WHERE project_id = ? AND category = ? ORDER BY created_at ASC", (project_id, category))
            else:
                cursor.execute("SELECT * FROM memory WHERE project_id = ? ORDER BY created_at ASC", (project_id,))
            return [dict(r) for r in cursor.fetchall()]
