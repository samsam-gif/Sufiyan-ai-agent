"""
CEO Agent: High-level orchestration, project planning, task delegation, and escalation handling.
"""
import uuid
import time
import json
from typing import Dict, Any, List
from backend.agents.base import BaseAgent

class CEOAgent(BaseAgent):
    def __init__(self, router, memory_store, approval_mgr, sandbox, db, event_bus=None):
        super().__init__("ceo", "Executive Orchestration", router, memory_store, approval_mgr, sandbox, db, event_bus)

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        project_id = task["project_id"]
        objective = task["objective"]
        
        self.update_state("RUNNING", 10, f"Analyzing directive: {objective[:30]}...", task["id"])
        self.log(project_id, "INFO", f"CEO received company directive: '{objective}'")

        # Call Model Router
        resp = await self.router.generate_response(
            prompt=f"Create a multi-department breakdown for objective: {objective}",
            system_instruction="You are the CEO of an autonomous software and design company. Provide strategic breakdown.",
            agent_name="ceo"
        )
        
        self.update_state("THINKING", 40, "Synthesizing project requirements", task["id"])
        self.memory.store_memory(project_id, "requirements", "core_scope", objective, "ceo")
        self.memory.store_memory(project_id, "strategy", "ceo_plan", resp["content"], "ceo")
        
        self.update_state("RUNNING", 70, "Delegating tasks across departments", task["id"])
        self.log(project_id, "INFO", f"CEO established project execution graph using {resp['provider']}")

        # Ensure project workspace directories are initialized
        self.sandbox.init_project_workspace(project_id)

        self.update_state("IDLE", 100, "Delegation complete. Tracking execution pipeline.", None)
        return {
            "success": True,
            "result": f"Project {project_id} initialized with departments assigned.",
            "provider": resp["provider"]
        }

    def create_project_pipeline(self, project_id: str, title: str, objective: str) -> List[str]:
        """Creates the formal sequential task chain for a project."""
        now = time.time()
        tasks = [
            ("TASK-001", "ceo", f"Architect requirements and plan for {title}", "HIGH", []),
            ("TASK-002", "design", f"Design responsive UI/UX architecture for {title}", "HIGH", ["TASK-001"]),
            ("TASK-003", "developer", f"Implement source code and build assets for {title}", "HIGH", ["TASK-002"]),
            ("TASK-004", "qa", f"Execute build verification and regression tests for {title}", "HIGH", ["TASK-003"]),
            ("TASK-005", "security", f"Conduct security audit and scope verification for {title}", "HIGH", ["TASK-004"]),
            ("TASK-006", "documentation", f"Generate technical documentation & runbooks for {title}", "MEDIUM", ["TASK-005"]),
            ("TASK-007", "deployment", f"Package build and stage production deployment for {title}", "HIGH", ["TASK-006"])
        ]
        
        created_ids = []
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            for tid, agent, obj, prio, deps in tasks:
                cursor.execute("""
                INSERT OR IGNORE INTO tasks (id, project_id, agent, objective, status, priority, dependencies, retry_count, max_retries, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'PENDING', ?, ?, 0, 3, ?, ?)
                """, (tid, project_id, agent, obj, prio, json.dumps(deps), now, now))
                created_ids.append(tid)
            conn.commit()
        return created_ids
