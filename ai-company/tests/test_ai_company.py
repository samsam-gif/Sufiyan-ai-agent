"""
Automated Test Suite for AI Company Command Center.
Tests Authentication, Model Router, Permissions, Approvals, Project Isolation, and E2E Workflow.
"""
import unittest
import asyncio
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.config import AppConfig
from backend.database.db import Database
from backend.core.security import SecurityManager
from backend.core.router import ModelRouter
from backend.permissions.policy import PermissionPolicy, RiskLevel
from backend.approvals.manager import ApprovalManager
from backend.services.sandbox import SandboxService
from backend.memory.store import MemoryStore
from backend.workers.engine import WorkerEngine

class TestAICompanySuite(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "./memory/test_company.db"
        self.test_proj_dir = "./projects_test"
        os.makedirs("./memory", exist_ok=True)
        os.makedirs(self.test_proj_dir, exist_ok=True)
        self.config = AppConfig(db_path=self.test_db_path, projects_dir=self.test_proj_dir)
        self.db = Database(self.test_db_path)
        self.sec = SecurityManager("test-secret-key")
        self.router = ModelRouter(self.config, self.db)
        self.policy = PermissionPolicy()
        self.approvals = ApprovalManager(self.db)
        self.sandbox = SandboxService(self.test_proj_dir)
        self.memory = MemoryStore(self.db)
        self.engine = WorkerEngine(self.db, self.router, self.memory, self.approvals, self.sandbox)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        if os.path.exists(self.test_proj_dir):
            shutil.rmtree(self.test_proj_dir, ignore_errors=True)

    def test_01_authentication_and_tokens(self):
        pwd = "secure_owner_password"
        phash = self.sec.hash_password(pwd)
        self.assertTrue(self.sec.verify_password(pwd, phash))
        self.assertFalse(self.sec.verify_password("wrong", phash))
        
        token = self.sec.create_token("owner", role="owner")
        decoded = self.sec.verify_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["sub"], "owner")
        self.assertEqual(decoded["role"], "owner")

    def test_02_model_router_fallback(self):
        status = self.router.get_provider_status()
        self.assertIn("overall_status", status)
        
        # Test generation without external provider
        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(self.router.generate_response("Build landing page", agent_name="developer"))
        loop.close()
        self.assertTrue(res["fallback_mode"])
        self.assertEqual(res["provider"], "Standalone Autonomous Engine")
        self.assertTrue(len(res["content"]) > 0)

    def test_03_permissions_and_risk_matrix(self):
        risk, req_app, _ = self.policy.evaluate_action("deployment", "Deploy production release")
        self.assertEqual(risk, RiskLevel.HIGH)
        self.assertTrue(req_app)

        risk, req_app, _ = self.policy.evaluate_action("developer", "read file index.html")
        self.assertEqual(risk, RiskLevel.LOW)
        self.assertFalse(req_app)

    def test_04_approvals_workflow(self):
        app_id = self.approvals.request_approval("PROJECT-001", "deployment", "Deploy to live server", "HIGH", "QA Passed")
        self.assertTrue(app_id.startswith("APP-"))
        
        pending = self.approvals.list_approvals("PENDING")
        self.assertEqual(len(pending), 1)
        
        resolved = self.approvals.resolve_approval(app_id, approved=True, reviewer="owner")
        self.assertTrue(resolved)
        
        approved_list = self.approvals.list_approvals("APPROVED")
        self.assertEqual(len(approved_list), 1)

    def test_05_sandbox_isolation_and_security(self):
        dirs = self.sandbox.init_project_workspace("PROJECT-001")
        self.assertTrue(os.path.exists(dirs["workspace"]))

        ok, msg = self.sandbox.write_project_file("PROJECT-001", "src/main.js", "console.log('safe');")
        self.assertTrue(ok)

        read_ok, content = self.sandbox.read_project_file("PROJECT-001", "src/main.js")
        self.assertTrue(read_ok)
        self.assertEqual(content, "console.log('safe');")

        # Traversal test
        invalid_ok, _ = self.sandbox.validate_path("PROJECT-001", "../../secret.txt")
        self.assertFalse(invalid_ok)

        # Forbidden command test
        cmd_res = self.sandbox.run_controlled_command("PROJECT-001", "rm -rf /")
        self.assertFalse(cmd_res["success"])
        self.assertIn("forbidden", cmd_res["stderr"].lower())

    def test_06_e2e_ceo_workflow_pipeline(self):
        """End-to-End test for: OWNER COMMAND -> CEO -> DESIGN -> DEVELOPER -> QA -> SECURITY -> DOCUMENTATION -> DELIVERY"""
        loop = asyncio.new_event_loop()
        
        # 1. CEO creates project & tasks
        ceo_agent = self.engine.agents["ceo"]
        task_ids = ceo_agent.create_project_pipeline("PROJECT-TEST-001", "Mobile Repair Shop Website", "Build professional responsive portal")
        self.assertEqual(len(task_ids), 7)

        # 2. Execute tasks in pipeline order via WorkerEngine
        executed_tasks = []
        for _ in range(6):
            tid = loop.run_until_complete(self.engine.process_next_task())
            if tid:
                executed_tasks.append(tid)

        self.assertIn("TASK-001", executed_tasks) # CEO
        self.assertIn("TASK-002", executed_tasks) # Design
        self.assertIn("TASK-003", executed_tasks) # Developer
        self.assertIn("TASK-004", executed_tasks) # QA
        self.assertIn("TASK-005", executed_tasks) # Security
        self.assertIn("TASK-006", executed_tasks) # Documentation
        
        # Check deployment task requires approval
        dep_task = loop.run_until_complete(self.engine.process_next_task())
        self.assertEqual(dep_task, "TASK-007")
        
        # Verify approval was created
        apps = self.approvals.list_approvals("PENDING")
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0]["agent"], "deployment")
        
        # Approve deployment
        self.approvals.resolve_approval(apps[0]["id"], approved=True)
        
        # Process final deployment task
        final_tid = loop.run_until_complete(self.engine.process_next_task())
        self.assertEqual(final_tid, "TASK-007")

        loop.close()

if __name__ == "__main__":
    unittest.main()
