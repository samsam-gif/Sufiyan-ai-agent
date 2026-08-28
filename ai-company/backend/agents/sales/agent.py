"""
Sales & Client Agents for AI Company.
Sales never sends external messages automatically by default.
Client Agent tracks customer specifications and questions.
"""
from backend.agents.base import BaseAgent
from typing import Dict, Any

class SalesAgent(BaseAgent):
    def __init__(self, router, memory_store, approval_mgr, sandbox, db, event_bus=None):
        super().__init__("sales", "Sales & Requirements", router, memory_store, approval_mgr, sandbox, db, event_bus)

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        project_id = task["project_id"]
        self.update_state("RUNNING", 20, "Drafting project commercial proposal & scope", task["id"])
        self.log(project_id, "INFO", f"Sales Agent analyzing customer brief for {project_id}")

        resp = await self.router.generate_response(
            prompt=f"Generate commercial proposal and requirements summary for: {task['objective']}",
            system_instruction="You are the Head of Sales. Draft a professional client proposal with deliverable scope and milestones.",
            agent_name="sales"
        )

        proposal = f"""# Commercial Proposal & Deliverable Scope
Target Project: {project_id}
Status: Draft (Pending Owner Approval for External Dispatch)

{resp['content']}
"""
        self.sandbox.write_project_file(project_id, "reports/proposal_draft.md", proposal)
        self.memory.store_memory(project_id, "sales", "proposal", proposal, "sales")
        self.log(project_id, "INFO", "Sales proposal drafted. (Note: External delivery held for approval)")
        self.update_state("IDLE", 100, "Proposal drafted.", None)
        return {"success": True, "result": "Sales proposal generated."}

class ClientAgent(BaseAgent):
    def __init__(self, router, memory_store, approval_mgr, sandbox, db, event_bus=None):
        super().__init__("client", "Client Communication", router, memory_store, approval_mgr, sandbox, db, event_bus)

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        project_id = task["project_id"]
        self.update_state("RUNNING", 30, "Processing client specifications and questions", task["id"])
        self.log(project_id, "INFO", f"Client Agent logged customer requirement updates for {project_id}")

        self.memory.store_memory(project_id, "client", "requirements_log", task["objective"], "client")
        self.update_state("IDLE", 100, "Client requirements reconciled.", None)
        return {"success": True, "result": "Client requirements processed."}
