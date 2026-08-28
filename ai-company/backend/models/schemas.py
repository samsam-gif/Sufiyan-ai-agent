"""
Data models and schemas for AI Company Command Center.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class ProjectSchema:
    id: str
    title: str
    objective: str
    status: str = "ACTIVE"
    progress: int = 0
    active_agent: str = "ceo"
    pipeline_stage: str = "Requirements"
    created_at: float = 0.0
    updated_at: float = 0.0

@dataclass
class TaskSchema:
    id: str
    project_id: str
    agent: str
    objective: str
    status: str = "PENDING"  # PENDING, QUEUED, RUNNING, WAITING, NEEDS_APPROVAL, COMPLETED, FAILED, CANCELLED
    priority: str = "MEDIUM" # LOW, MEDIUM, HIGH, CRITICAL
    dependencies: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: float = 0.0
    updated_at: float = 0.0

@dataclass
class AgentStateSchema:
    name: str
    department: str
    status: str = "IDLE" # RUNNING, WAITING, THINKING, NEEDS_APPROVAL, ERROR, IDLE
    current_task_id: Optional[str] = None
    progress: int = 0
    last_action: str = ""
    updated_at: float = 0.0

@dataclass
class ApprovalSchema:
    id: str
    project_id: str
    task_id: Optional[str]
    agent: str
    action: str
    risk_level: str # LOW, MEDIUM, HIGH
    reason: str
    status: str = "PENDING" # PENDING, APPROVED, REJECTED
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[float] = None
    created_at: float = 0.0

@dataclass
class LogSchema:
    id: Optional[int]
    project_id: Optional[str]
    agent: str
    level: str
    message: str
    timestamp: float

@dataclass
class SystemHealthSchema:
    backend: str = "HEALTHY"
    database: str = "HEALTHY"
    workers: str = "RUNNING"
    websocket: str = "ONLINE"
    ai_providers: str = "NOT_CONFIGURED"
    active_tasks: int = 0
    total_projects: int = 0
    system_memory_mb: float = 0.0
    disk_usage_pct: float = 0.0
