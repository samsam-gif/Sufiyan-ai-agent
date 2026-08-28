"""
Database management for AI Company Command Center using SQLite.
Supports persistent projects, tasks, approvals, agent states, memories, and audit logs.
"""
import sqlite3
import os
import json
import time
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, db_path: str = "./memory/company.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'owner',
                created_at REAL NOT NULL
            )
            """)
            
            # Projects
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                objective TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                progress INTEGER NOT NULL DEFAULT 0,
                active_agent TEXT DEFAULT 'ceo',
                pipeline_stage TEXT DEFAULT 'Requirements',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """)
            
            # Tasks
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                agent TEXT NOT NULL,
                objective TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                priority TEXT NOT NULL DEFAULT 'MEDIUM',
                dependencies TEXT NOT NULL DEFAULT '[]',
                retry_count INTEGER NOT NULL DEFAULT 0,
                max_retries INTEGER NOT NULL DEFAULT 3,
                result TEXT,
                error_message TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
            """)
            
            # Agent Status
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_states (
                name TEXT PRIMARY KEY,
                department TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'IDLE',
                current_task_id TEXT,
                progress INTEGER NOT NULL DEFAULT 0,
                last_action TEXT DEFAULT '',
                updated_at REAL NOT NULL
            )
            """)
            
            # Approvals
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                task_id TEXT,
                agent TEXT NOT NULL,
                action TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                reviewed_by TEXT,
                reviewed_at REAL,
                created_at REAL NOT NULL
            )
            """)
            
            # Memory (Project Scoped)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                agent TEXT NOT NULL,
                created_at REAL NOT NULL
            )
            """)
            
            # Logs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                agent TEXT NOT NULL,
                level TEXT NOT NULL DEFAULT 'INFO',
                message TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
            """)
            
            # Audit Logs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT NOT NULL,
                action TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                command TEXT,
                status TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
            """)
            
            # Model Providers state & stats
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_providers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                base_url TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 0,
                priority INTEGER NOT NULL DEFAULT 1,
                timeout_sec INTEGER NOT NULL DEFAULT 30,
                total_calls INTEGER NOT NULL DEFAULT 0,
                successful_calls INTEGER NOT NULL DEFAULT 0,
                failed_calls INTEGER NOT NULL DEFAULT 0,
                avg_latency_ms REAL NOT NULL DEFAULT 0.0
            )
            """)
            
            conn.commit()
            self._seed_default_agents(conn)
            self._seed_default_providers(conn)

    def _seed_default_agents(self, conn: sqlite3.Connection):
        departments = [
            ("ceo", "Executive Orchestration"),
            ("sales", "Sales & Requirements"),
            ("client", "Client Communication"),
            ("design", "UI/UX Architecture"),
            ("developer", "Software Engineering"),
            ("qa", "Quality Assurance"),
            ("security", "Cybersecurity & Audit"),
            ("deployment", "Release & DevOps"),
            ("documentation", "Technical Documentation")
        ]
        cursor = conn.cursor()
        now = time.time()
        for name, dept in departments:
            cursor.execute("""
            INSERT OR IGNORE INTO agent_states (name, department, status, progress, last_action, updated_at)
            VALUES (?, ?, 'IDLE', 0, 'Standing by', ?)
            """, (name, dept, now))
        conn.commit()

    def _seed_default_providers(self, conn: sqlite3.Connection):
        providers = [
            ("gemini", "Google Gemini", "https://generativelanguage.googleapis.com/v1beta", 0, 1, 30),
            ("openai", "OpenAI", "https://api.openai.com/v1", 0, 2, 30),
            ("anthropic", "Anthropic Claude", "https://api.anthropic.com/v1", 0, 3, 30),
            ("custom", "Custom Provider", "https://api.custom-ai.com/v1", 0, 4, 30),
        ]
        cursor = conn.cursor()
        for pid, name, url, enabled, prio, timeout in providers:
            cursor.execute("""
            INSERT OR IGNORE INTO model_providers 
            (id, name, base_url, enabled, priority, timeout_sec, total_calls, successful_calls, failed_calls, avg_latency_ms)
            VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0, 0.0)
            """, (pid, name, url, enabled, prio, timeout))
        conn.commit()
