#!/usr/bin/env bash
# AI Company Command Center - Shutdown Script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "Stopping AI Company Command Center..."
if [ -f "logs/backend.pid" ]; then
    PID=$(cat logs/backend.pid)
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID" || kill -9 "$PID"
        echo "Backend stopped (PID: $PID)."
    else
        echo "Backend process $PID was not running."
    fi
    rm -f logs/backend.pid
else
    echo "No backend PID file found. Checking for lingering python backend processes..."
    pkill -f "backend/main.py" || true
    echo "Cleaned up."
fi
