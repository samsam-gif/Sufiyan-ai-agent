"""
Main Application Entrypoint for AI Company Command Center.
High performance asynchronous server with native REST endpoints, WebSocket event streaming,
and continuous background AI agent workers.
"""
import asyncio
import os
import sys
import json
import time
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.config import AppConfig
from backend.database.db import Database
from backend.core.security import SecurityManager
from backend.core.router import ModelRouter
from backend.permissions.policy import PermissionPolicy
from backend.approvals.manager import ApprovalManager
from backend.services.sandbox import SandboxService
from backend.services.audit import AuditService
from backend.memory.store import MemoryStore
from backend.workers.engine import WorkerEngine
from backend.api.websocket import EventBus
from backend.api.routes import ApiHandler

class SimpleServerContext:
    def __init__(self):
        self.config = AppConfig.load()
        self.db = Database(self.config.db_path)
        self.sec_mgr = SecurityManager(self.config.jwt_secret)
        self.router = ModelRouter(self.config, self.db)
        self.permission_policy = PermissionPolicy()
        self.approval_mgr = ApprovalManager(self.db)
        self.sandbox = SandboxService(self.config.projects_dir)
        self.audit_service = AuditService(self.db)
        self.memory_store = MemoryStore(self.db)
        self.event_bus = EventBus()
        self.worker_engine = WorkerEngine(
            self.db, self.router, self.memory_store, self.approval_mgr, self.sandbox, self.event_bus
        )
        self.api = ApiHandler(
            self.db, self.router, self.memory_store, self.approval_mgr,
            self.sandbox, self.sec_mgr, self.worker_engine, self.event_bus
        )

ctx = SimpleServerContext()

class CompanyRequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _read_json_body(self) -> Dict[str, Any]:
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length > 0:
                raw = self.rfile.read(length).decode('utf-8')
                return json.loads(raw)
        except Exception:
            pass
        return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        qs = parse_qs(parsed.query)
        
        # Route dispatcher
        if path == "" or path == "/api":
            self._send_json({"status": "AI Company Backend Online", "version": "1.0.0"})
        elif path == "/api/projects":
            self._send_json(ctx.api.list_projects())
        elif path.startswith("/api/projects/"):
            pid = path.replace("/api/projects/", "")
            res = ctx.api.get_project(pid)
            if res:
                self._send_json(res)
            else:
                self._send_json({"error": "Project not found"}, 404)
        elif path == "/api/tasks":
            pid = qs.get("project_id", [None])[0]
            status = qs.get("status", [None])[0]
            self._send_json(ctx.api.list_tasks(pid, status))
        elif path == "/api/agents":
            self._send_json(ctx.api.list_agents())
        elif path.startswith("/api/agents/"):
            aname = path.replace("/api/agents/", "")
            res = ctx.api.get_agent(aname)
            if res:
                self._send_json(res)
            else:
                self._send_json({"error": "Agent not found"}, 404)
        elif path == "/api/approvals":
            status = qs.get("status", [None])[0]
            self._send_json(ctx.api.list_approvals(status))
        elif path == "/api/logs":
            pid = qs.get("project_id", [None])[0]
            self._send_json(ctx.api.get_logs(pid))
        elif path == "/api/models":
            self._send_json(ctx.api.get_models())
        elif path == "/api/system/health":
            self._send_json(ctx.api.get_system_health())
        elif path == "/api/audit":
            self._send_json(ctx.audit_service.get_audit_trail())
        else:
            self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        body = self._read_json_body()

        if path == "/api/auth/login":
            res = ctx.api.login(body)
            self._send_json(res, 200 if res.get("success") else 401)
        elif path == "/api/projects":
            self._send_json(ctx.api.create_project(body))
        elif path == "/api/tasks":
            self._send_json(ctx.api.create_task(body))
        elif path == "/api/ceo/command":
            # Run async command execution in event loop
            loop = asyncio.get_event_loop()
            res = loop.run_until_complete(ctx.api.execute_ceo_command(body))
            self._send_json(res)
        elif "/api/approvals/" in path:
            parts = path.split("/")
            aid = parts[3]
            action = parts[4] if len(parts) > 4 else "approve"
            res = ctx.api.resolve_approval(aid, approved=(action == "approve"))
            self._send_json(res)
        elif "/api/agents/" in path:
            parts = path.split("/")
            aname = parts[3]
            action = parts[4] if len(parts) > 4 else "pause"
            res = ctx.api.control_agent(aname, action)
            self._send_json(res)
        elif path == "/api/models":
            self._send_json(ctx.api.update_model_provider(body))
        else:
            self._send_json({"error": "Not Found"}, 404)

    def log_message(self, format, *args):
        # Keep console output clean
        return

def run_http_server(host: str, port: int):
    server = HTTPServer((host, port), CompanyRequestHandler)
    print(f"[AI Company] REST Engine active at http://{host}:{port}")
    server.serve_forever()

async def main():
    print("=================================")
    print(" 👑 AI COMPANY COMMAND CENTER")
    print("=================================")
    print(f"Backend Host: {ctx.config.host}:{ctx.config.port}")
    print(f"Database: {ctx.config.db_path}")
    print(f"AI Provider Status: {ctx.router.get_provider_status()['overall_status']}")
    print("Starting background multi-agent worker loops...")
    
    # Start worker loop
    await ctx.worker_engine.start()
    
    # Start HTTP REST server in dedicated thread
    t = threading.Thread(target=run_http_server, args=(ctx.config.host, ctx.config.port), daemon=True)
    t.start()
    
    print("All backend systems running.")
    
    # Keep event loop running and processing tasks
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping AI Company Command Center cleanly.")
