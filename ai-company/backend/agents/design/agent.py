"""
Design Agent: UI/UX architecture, responsive component layouts, color tokens, and accessibility.
"""
from backend.agents.base import BaseAgent
from typing import Dict, Any

class DesignAgent(BaseAgent):
    def __init__(self, router, memory_store, approval_mgr, sandbox, db, event_bus=None):
        super().__init__("design", "UI/UX Architecture", router, memory_store, approval_mgr, sandbox, db, event_bus)

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        project_id = task["project_id"]
        self.update_state("RUNNING", 15, "Drafting UI/UX specs and responsive structure", task["id"])
        self.log(project_id, "INFO", "Design Agent starting layout hierarchy & color tokens")

        resp = await self.router.generate_response(
            prompt=f"Create a modern, responsive UI design specification for: {task['objective']}",
            system_instruction="You are the Lead UI/UX Designer. Specify layout structure, CSS color palette tokens, typography, and component hierarchy.",
            agent_name="design"
        )

        self.update_state("THINKING", 60, "Generating design token assets in workspace", task["id"])
        
        design_spec = f"""/* Design Specification for Project {project_id} */
:root {{
  --color-primary: #0F172A;
  --color-accent: #38BDF8;
  --color-surface: #1E293B;
  --color-text: #F8FAFC;
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius-sm: 8px;
  --radius-md: 16px;
}}
/* Component Architecture */
/* {resp['content']} */
"""
        self.sandbox.write_project_file(project_id, "styles/theme.css", design_spec)
        self.memory.store_memory(project_id, "design", "tokens", design_spec, "design")

        self.log(project_id, "INFO", "Design specs and styles/theme.css generated successfully.")
        self.update_state("IDLE", 100, "Design assets delivered.", None)
        return {"success": True, "result": "Design tokens and UI specs created."}
