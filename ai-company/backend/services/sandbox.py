"""
Sandbox Execution & Workspace Isolation for Developer and other agents.
Strictly isolates projects in their designated directory: projects/PROJECT-XXX/workspace.
Guards against directory traversal and destructive shell commands.
"""
import os
import subprocess
import shlex
import time
from typing import Tuple, Dict, Any, List

class SandboxService:
    FORBIDDEN_COMMANDS = [
        "rm -rf /", "mkfs", "dd if=", ":(){ :|:& };:", "chmod -R 777 /",
        "shutdown", "reboot", "init 0", "nc -e", "/bin/sh -i", "userdel", "passwd"
    ]

    def __init__(self, base_projects_dir: str = "./projects"):
        self.base_projects_dir = os.path.abspath(base_projects_dir)
        os.makedirs(self.base_projects_dir, exist_ok=True)

    def init_project_workspace(self, project_id: str) -> Dict[str, str]:
        """Creates isolated workspace, memory, reports, and logs directories for a project."""
        pdir = os.path.join(self.base_projects_dir, project_id)
        dirs = {
            "root": pdir,
            "workspace": os.path.join(pdir, "workspace"),
            "memory": os.path.join(pdir, "memory"),
            "reports": os.path.join(pdir, "reports"),
            "logs": os.path.join(pdir, "logs")
        }
        for d in dirs.values():
            os.makedirs(d, exist_ok=True)
        return dirs

    def validate_path(self, project_id: str, relative_path: str) -> Tuple[bool, str]:
        """Ensures file access stays strictly inside project workspace."""
        workspace = os.path.join(self.base_projects_dir, project_id, "workspace")
        target = os.path.abspath(os.path.join(workspace, relative_path))
        if not target.startswith(os.path.abspath(workspace)):
            return False, "Path traversal attempt detected. Access denied."
        return True, target

    def write_project_file(self, project_id: str, relative_path: str, content: str) -> Tuple[bool, str]:
        valid, target = self.validate_path(project_id, relative_path)
        if not valid:
            return False, target
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return True, f"Successfully created {relative_path}"

    def read_project_file(self, project_id: str, relative_path: str) -> Tuple[bool, str]:
        valid, target = self.validate_path(project_id, relative_path)
        if not valid:
            return False, target
        if not os.path.exists(target):
            return False, f"File {relative_path} does not exist"
        with open(target, "r", encoding="utf-8") as f:
            return True, f.read()

    def run_controlled_command(self, project_id: str, command: str, timeout_sec: int = 15) -> Dict[str, Any]:
        """Executes safe commands strictly inside project workspace."""
        workspace = os.path.join(self.base_projects_dir, project_id, "workspace")
        os.makedirs(workspace, exist_ok=True)

        for forbidden in self.FORBIDDEN_COMMANDS:
            if forbidden in command:
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Security Policy Violation: Command '{forbidden}' is forbidden.",
                    "exit_code": 126
                }

        try:
            res = subprocess.run(
                command,
                shell=True,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout[:5000],
                "stderr": res.stderr[:5000],
                "exit_code": res.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Execution timed out after {timeout_sec} seconds.",
                "exit_code": 124
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1
            }
