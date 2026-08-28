"""
Real-time WebSocket connection manager and event bus for AI Company Command Center.
"""
import asyncio
import json
import time
from typing import List, Dict, Any, Callable

class EventBus:
    def __init__(self):
        self.subscribers: List[Callable[[str, Dict[str, Any]], None]] = []
        self.active_connections: List[Any] = []

    def subscribe(self, callback: Callable[[str, Dict[str, Any]], None]):
        self.subscribers.append(callback)

    def register_client(self, websocket):
        self.active_connections.append(websocket)

    def unregister_client(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    def publish(self, event_type: str, data: Dict[str, Any]):
        payload = {
            "event": event_type,
            "data": data,
            "timestamp": time.time()
        }
        for sub in self.subscribers:
            try:
                sub(event_type, payload)
            except Exception:
                pass

        # Broadcast to active WebSockets
        for ws in list(self.active_connections):
            try:
                if hasattr(ws, "send_text"):
                    asyncio.create_task(ws.send_text(json.dumps(payload)))
                elif hasattr(ws, "send"):
                    ws.send(json.dumps(payload))
            except Exception:
                self.unregister_client(ws)
