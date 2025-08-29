"""
WebSocket endpoint for real-time progress updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import asyncio
from datetime import datetime

router = APIRouter()

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.progress_data: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = set()
        self.active_connections[client_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id].discard(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
    
    async def send_progress(self, client_id: str, data: dict):
        """Send progress update to specific client"""
        if client_id in self.active_connections:
            disconnected = set()
            for websocket in self.active_connections[client_id]:
                try:
                    await websocket.send_json(data)
                except:
                    disconnected.add(websocket)
            
            # Remove disconnected websockets
            for ws in disconnected:
                self.active_connections[client_id].discard(ws)
    
    async def broadcast_progress(self, business_id: str, progress_type: str, data: dict):
        """Broadcast progress to all connected clients interested in a business"""
        message = {
            "type": progress_type,
            "business_id": business_id,
            "timestamp": datetime.now().isoformat(),
            **data
        }
        
        # Store latest progress
        if business_id not in self.progress_data:
            self.progress_data[business_id] = {}
        self.progress_data[business_id][progress_type] = message
        
        # Send to all connections
        for client_id in list(self.active_connections.keys()):
            await self.send_progress(client_id, message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif message.get("type") == "subscribe":
                business_id = message.get("business_id")
                if business_id and business_id in manager.progress_data:
                    # Send latest progress data for this business
                    for progress_type, progress_data in manager.progress_data[business_id].items():
                        await websocket.send_json(progress_data)
                        
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, client_id)

# Helper function to send progress updates from other parts of the app
async def send_research_progress(business_id: str, step: str, progress: float, message: str):
    """Send research progress update"""
    await manager.broadcast_progress(
        business_id=business_id,
        progress_type="research_progress",
        data={
            "step": step,
            "progress": progress,
            "message": message,
            "status": "in_progress" if progress < 100 else "completed"
        }
    )

async def send_generation_progress(business_id: str, step: str, progress: float, message: str):
    """Send website generation progress update"""
    await manager.broadcast_progress(
        business_id=business_id,
        progress_type="generation_progress",
        data={
            "step": step,
            "progress": progress,
            "message": message,
            "status": "in_progress" if progress < 100 else "completed"
        }
    )