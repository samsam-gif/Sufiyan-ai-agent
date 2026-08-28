"""
Base Agent definition for AI Company background workers.
"""
import time
from typing import Dict, Any, Optional

class BaseAgent:
    def __init__(self, name: str, department: str, router, memory_store, approval_mgr, sandbox, db, event_bus=None):
        self.name = name
        self.department = department
        self.router = router
        self.memory = memory_store
        self.approval_mgr = approval_mgr
        self.sandbox = sandbox
        self.db = db
        self.event_bus = event_bus

    def log(self, project_id: Optional[str], level: str, message: str):
        now = time.time()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO logs (project_id, agent, level, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """, (project_id, self.name, level, message, now))
            conn.commit()
        
        if self.event_bus:
            self.event_bus.publish("log.created", {
                "project_id": project_id,
                "agent": self.name,
                "level": level,
                "message": message,
                "timestamp": now
            })

    def update_state(self, status: str, progress: int, last_action: str, current_task_id: Optional[str] = None):
        now = time.time()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE agent_states
            SET status = ?, progress = ?, last_action = ?, current_task_id = ?, updated_at = ?
            WHERE name = ?
            """, (status, progress, last_action, current_task_id, now, self.name))
            conn.commit()
            
        if self.event_bus:
            self.event_bus.publish(f"agent.{status.lower()}", {
                "agent": self.name,
                "status": status,
                "progress": progress,
                "last_action": last_action,
                "task_id": current_task_id
            })

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement execute_task")
