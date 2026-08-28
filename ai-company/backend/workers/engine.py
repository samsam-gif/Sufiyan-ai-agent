"""
Asynchronous Background Worker Engine for AI Company.
Polls persistent task queue, resolves dependencies, coordinates agent workers,
handles automatic retries, and escalates to CEO/Owner on repeated failure.
Runs independently of browser sessions.
"""
import asyncio
import time
import json
from typing import Dict, Any, List, Optional
from backend.agents.ceo.agent import CEOAgent
from backend.agents.design.agent import DesignAgent
from backend.agents.developer.agent import DeveloperAgent
from backend.agents.qa.agent import QAAgent
from backend.agents.security.agent import SecurityAgent
from backend.agents.deployment.agent import DeploymentAgent, DocumentationAgent
from backend.agents.sales.agent import SalesAgent, ClientAgent

class WorkerEngine:
    def __init__(self, db, router, memory_store, approval_mgr, sandbox, event_bus=None):
        self.db = db
        self.router = router
        self.memory_store = memory_store
        self.approval_mgr = approval_mgr
        self.sandbox = sandbox
        self.event_bus = event_bus
        self.is_running = False
        self._worker_task = None
        
        # Instantiate agents
        self.agents: Dict[str, Any] = {
            "ceo": CEOAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "design": DesignAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "developer": DeveloperAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "qa": QAAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "security": SecurityAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "deployment": DeploymentAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "documentation": DocumentationAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "sales": SalesAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
            "client": ClientAgent(router, memory_store, approval_mgr, sandbox, db, event_bus),
        }

    async def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._worker_task = asyncio.create_task(self._main_worker_loop())

    async def stop(self):
        self.is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def _main_worker_loop(self):
        while self.is_running:
            try:
                await self.process_next_task()
            except Exception as e:
                pass
            await asyncio.sleep(1.0)

    async def process_next_task(self) -> Optional[str]:
        task = self._fetch_ready_task()
        if not task:
            return None

        task_id = task["id"]
        agent_name = task["agent"].lower()
        project_id = task["project_id"]
        
        agent = self.agents.get(agent_name)
        if not agent:
            self._mark_task_failed(task_id, f"Unknown agent: {agent_name}")
            return task_id

        # Mark as RUNNING
        self._update_task_status(task_id, "RUNNING")
        self._update_project_pipeline(project_id, agent_name)

        try:
            result = await agent.execute_task(task)
            
            if result.get("needs_approval"):
                self._update_task_status(task_id, "NEEDS_APPROVAL", result=result.get("result"))
            elif result.get("success"):
                self._update_task_status(task_id, "COMPLETED", result=result.get("result"))
                self._check_project_completion(project_id)
            else:
                self._handle_task_failure(task, result.get("error", "Execution returned failure"))
        except Exception as e:
            self._handle_task_failure(task, str(e))

        return task_id

    def _fetch_ready_task(self) -> Optional[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM tasks 
            WHERE status IN ('PENDING', 'QUEUED') 
            ORDER BY 
                CASE priority WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END,
                created_at ASC
            """)
            tasks = [dict(r) for r in cursor.fetchall()]

            for t in tasks:
                # Check dependencies
                deps = json.loads(t.get("dependencies") or "[]")
                if not deps:
                    return t
                
                # Verify all dependency tasks are COMPLETED
                placeholders = ",".join("?" for _ in deps)
                cursor.execute(f"SELECT COUNT(*) as cnt FROM tasks WHERE id IN ({placeholders}) AND status = 'COMPLETED'", deps)
                completed_cnt = cursor.fetchone()["cnt"]
                if completed_cnt == len(deps):
                    return t
        return None

    def _update_task_status(self, task_id: str, status: str, result: Optional[str] = None, error: Optional[str] = None):
        now = time.time()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE tasks 
            SET status = ?, result = COALESCE(?, result), error_message = ?, updated_at = ?
            WHERE id = ?
            """, (status, result, error, now, task_id))
            conn.commit()

        if self.event_bus:
            self.event_bus.publish(f"task.{status.lower()}", {
                "task_id": task_id,
                "status": status,
                "result": result,
                "error": error
            })

    def _handle_task_failure(self, task: Dict[str, Any], error_msg: str):
        retries = task.get("retry_count", 0) + 1
        max_retries = task.get("max_retries", 3)
        now = time.time()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if retries <= max_retries:
                # Auto retry with backoff
                cursor.execute("""
                UPDATE tasks 
                SET status = 'QUEUED', retry_count = ?, error_message = ?, updated_at = ?
                WHERE id = ?
                """, (retries, f"Attempt {retries} failed: {error_msg}. Retrying...", now, task["id"]))
                conn.commit()
            else:
                # Retry limit exceeded -> Escalate to CEO / Owner
                cursor.execute("""
                UPDATE tasks 
                SET status = 'FAILED', retry_count = ?, error_message = ?, updated_at = ?
                WHERE id = ?
                """, (retries, f"Max retries ({max_retries}) exceeded: {error_msg}", now, task["id"]))
                conn.commit()
                # Create escalation approval/attention
                self.approval_mgr.request_approval(
                    project_id=task["project_id"],
                    agent="ceo",
                    action=f"Task {task['id']} Failed: Escalation Review",
                    risk_level="HIGH",
                    reason=f"Agent {task['agent']} exceeded retry limit on '{task['objective']}'. Requires Owner/CEO intervention.",
                    task_id=task["id"]
                )

    def _update_project_pipeline(self, project_id: str, agent_name: str):
        now = time.time()
        stage_map = {
            "ceo": ("Requirements", 10),
            "design": ("Design", 30),
            "developer": ("Development", 55),
            "qa": ("QA", 75),
            "security": ("Security Review", 85),
            "documentation": ("Documentation", 90),
            "deployment": ("Delivery", 95)
        }
        stage, prog = stage_map.get(agent_name, ("Processing", 50))
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE projects 
            SET active_agent = ?, pipeline_stage = ?, progress = MAX(progress, ?), updated_at = ?
            WHERE id = ?
            """, (agent_name, stage, prog, now, project_id))
            conn.commit()

    def _check_project_completion(self, project_id: str):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN status='COMPLETED' THEN 1 ELSE 0 END) as comp FROM tasks WHERE project_id = ?", (project_id,))
            row = cursor.fetchone()
            if row and row["total"] > 0 and row["total"] == row["comp"]:
                now = time.time()
                cursor.execute("UPDATE projects SET status = 'COMPLETED', progress = 100, pipeline_stage = 'Delivered', updated_at = ? WHERE id = ?", (now, project_id))
                conn.commit()
