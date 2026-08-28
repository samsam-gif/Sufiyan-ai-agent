#!/usr/bin/env bash
# AI Company Command Center - Startup Script
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo " 👑 AI COMPANY COMMAND CENTER - STARTING SERVICES"
echo "=================================================="

# 1. Environment verification
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required but not found."
    exit 1
fi

mkdir -p memory projects reports logs data

# 2. Check if already running
if [ -f "logs/backend.pid" ]; then
    PID=$(cat logs/backend.pid)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "[INFO] Backend is already running (PID: $PID)."
    else
        rm logs/backend.pid
    fi
fi

# 3. Start Backend in Background
echo "[1/2] Starting AI Company Backend & Worker Engine..."
python3 backend/main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > logs/backend.pid
sleep 1.5

# 4. Check Backend Status
if ps -p "$BACKEND_PID" > /dev/null 2>&1; then
    echo "  -> Backend running successfully (PID: $BACKEND_PID)"
else
    echo "  -> Backend start failed. Check logs/backend.log"
    exit 1
fi

echo "=================================================="
echo " 🚀 ALL SYSTEMS OPERATIONAL"
echo "=================================================="
echo " Backend REST API : http://127.0.0.1:8000"
echo " WebSocket Stream : ws://127.0.0.1:8000/ws"
echo " Native Android   : com.aistudio.aicompanymaster.qzkvm"
echo " Log output file  : logs/backend.log"
echo "=================================================="
echo "Use ./status.sh to check health, ./stop.sh to shutdown."
