# 👑 AI Company Command Center

An enterprise multi-agent company orchestration system with Kali Linux First + Future Android Architecture.

## Architecture Overview

```
                      👑 OWNER / CEO
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
        Web Dashboard                Android App
          (React/Web)             (Native Jetpack Compose)
              │                           │
              └─────────────┬─────────────┘
                            ▼
                     REST + WebSocket
                            │
                            ▼
                     FASTAPI BACKEND
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
    TASK QUEUE         MODEL ROUTER         APPROVALS
        │                   │                   │
        ▼                   ▼                   ▼
   AI WORKERS         EXTERNAL APIs          SECURITY
        │          (Gemini/OpenAI/Claude)
 ┌──────┼────────────┬──────────┬──────────┬──────────┐
 ▼      ▼            ▼          ▼          ▼          ▼
CEO   SALES        DESIGN      DEV        QA       SECURITY
                                                      │
                                                      ▼
                                                 DEPLOYMENT
                                                      │
                                                      ▼
                                                   DELIVERY
```

## Department Responsibilities

- **CEO**: High-level planning, delegation, project orchestration, and escalation resolution.
- **Sales**: Customer briefs, commercial proposals, requirements scoping. *(Never auto-dispatches external messages).*
- **Client**: Customer requirements, questions, scope changes.
- **Design**: UI/UX architecture, responsive layouts, design tokens (`styles/theme.css`), accessibility.
- **Developer**: Workspace code generation (`index.html`, `app.js`), build executions, automated syntax error recovery.
- **QA**: Independent test execution, 14-point validation checks, bug detection, QA reports.
- **Security**: Authorized project boundary reviews, CSP enforcement, injection checks, path traversal mitigation.
- **Documentation**: Technical runbooks, API documentation, component specifications.
- **Deployment**: Production build packaging (`workspace/dist/`), release staging, Owner Approval enforcement.

## Zero Dependency Mode & Model Router

The system runs **out of the box on vanilla Python 3.11** without requiring external pip dependencies or Ollama.
If no AI provider is configured in `.env`, the **Autonomous Standalone Engine** runs deterministic multi-agent plans automatically while clearly reporting:
```
AI Provider: NOT CONFIGURED
```

## Startup Instructions

### 1. Start Services
```bash
cd ai-company
chmod +x start.sh stop.sh status.sh
./start.sh
```

### 2. Check Service Health
```bash
./status.sh
```

### 3. Run Automated Tests
```bash
python3 tests/test_ai_company.py
```

### 4. Stop Services
```bash
./stop.sh
```

## REST API Endpoints

- `POST /api/auth/login` - Owner authentication & JWT issuance
- `GET /api/projects` - List all projects
- `POST /api/projects` - Create new project
- `GET /api/projects/{id}` - Project details, task breakdown, memories
- `POST /api/ceo/command` - Execute executive company directive
- `GET /api/tasks` - List tasks by status/project
- `POST /api/tasks` - Create standalone task
- `GET /api/agents` - List 9 AI department agent states
- `POST /api/agents/{id}/{pause|resume|stop}` - Agent operational controls
- `GET /api/approvals` - List pending/resolved owner approvals
- `POST /api/approvals/{id}/{approve|reject}` - Owner approval resolution
- `GET /api/logs` - Live structured log stream
- `GET /api/models` - Model router provider status & telemetry
- `GET /api/system/health` - Live system health metrics
- `WS /ws` - Real-time WebSocket event streaming

## Future Android Architecture

The Android application (`app/src/main/...`) is designed as a direct client of the FastAPI backend.
All worker logic, agent orchestrations, memory stores, and model routing remain securely on the backend server.
