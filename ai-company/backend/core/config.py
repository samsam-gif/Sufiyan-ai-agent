"""
Configuration management for AI Company Command Center.
"""
import os
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class ProviderConfig:
    name: str
    base_url: str = ""
    api_key: str = ""
    models: List[str] = field(default_factory=list)
    timeout_sec: int = 30
    retry_limit: int = 3
    priority: int = 1
    enabled: bool = False

@dataclass
class AppConfig:
    env: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    db_path: str = "./memory/company.db"
    projects_dir: str = "./projects"
    logs_dir: str = "./logs"
    reports_dir: str = "./reports"
    jwt_secret: str = "ai-company-master-secret-key-2026"
    owner_username: str = "owner"
    owner_password_hash: str = "" # SHA-256
    providers: Dict[str, ProviderConfig] = field(default_factory=dict)
    
    @classmethod
    def load(cls, env_path: str = ".env") -> "AppConfig":
        config = cls()
        # Default owner password hash for 'admin123' or from env
        import hashlib
        default_pwd_hash = hashlib.sha256("admin123".encode()).hexdigest()
        config.owner_password_hash = os.getenv("OWNER_PASSWORD_HASH", default_pwd_hash)
        config.host = os.getenv("APP_HOST", "127.0.0.1")
        config.port = int(os.getenv("APP_PORT", "8000"))
        config.jwt_secret = os.getenv("SECRET_KEY", "ai-company-master-secret-key-2026")
        
        # Load providers
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        openai_key = os.getenv("OPENAI_API_KEY", "")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        custom_key = os.getenv("CUSTOM_AI_API_KEY", "")
        
        config.providers["gemini"] = ProviderConfig(
            name="Google Gemini",
            base_url="https://generativelanguage.googleapis.com/v1beta",
            api_key=gemini_key,
            models=["gemini-2.5-flash", "gemini-2.5-pro"],
            enabled=bool(gemini_key),
            priority=1
        )
        config.providers["openai"] = ProviderConfig(
            name="OpenAI",
            base_url="https://api.openai.com/v1",
            api_key=openai_key,
            models=["gpt-4o", "gpt-4o-mini"],
            enabled=bool(openai_key),
            priority=2
        )
        config.providers["anthropic"] = ProviderConfig(
            name="Anthropic Claude",
            base_url="https://api.anthropic.com/v1",
            api_key=anthropic_key,
            models=["claude-3-5-sonnet", "claude-3-5-haiku"],
            enabled=bool(anthropic_key),
            priority=3
        )
        config.providers["custom"] = ProviderConfig(
            name="Custom Provider",
            base_url=os.getenv("CUSTOM_AI_BASE_URL", "https://api.custom-ai.com/v1"),
            api_key=custom_key,
            models=["custom-model-1"],
            enabled=bool(custom_key),
            priority=4
        )
        return config
