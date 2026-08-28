#!/usr/bin/env bash
# AI Company Command Center - Status Script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo " 👑 AI COMPANY COMMAND CENTER - STATUS REPORT"
echo "=================================================="

if [ -f "logs/backend.pid" ]; then
    PID=$(cat logs/backend.pid)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Backend Service : 🟢 RUNNING (PID: $PID)"
    else
        echo "Backend Service : 🔴 STOPPED (Stale PID: $PID)"
    fi
else
    echo "Backend Service : ⚪ NOT RUNNING"
fi

echo "--------------------------------------------------"
echo "Live System Health Check via REST API:"
python3 -c '
import urllib.request, json
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/system/health", timeout=2) as resp:
        data = json.loads(resp.read().decode())
        print(f"  Backend      : {data.get(\"backend\", \"UNKNOWN\")}")
        print(f"  Database     : {data.get(\"database\", \"UNKNOWN\")}")
        print(f"  Workers      : {data.get(\"workers\", \"UNKNOWN\")}")
        print(f"  AI Providers : {data.get(\"ai_providers\", \"UNKNOWN\")}")
        print(f"  Total Projects: {data.get(\"total_projects\", 0)}")
except Exception as e:
    print(f"  REST API Unreachable: {e}")
'
echo "=================================================="
