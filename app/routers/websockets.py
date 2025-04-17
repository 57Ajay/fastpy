from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends
from typing import List, Annotated
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)
        print(f"New connection. Total connections: {len(self.active_connections)}")
    async def close(self, ws: WebSocket):
        if ws in self.active_connections:
            self.active_connections.remove(ws)
        print(f"A connection has been closed: Total connections: {len(self.active_connections)}")
    async def send_personal_message(self, message: str, ws: WebSocket):
        await ws.send_text(message)
    async def broadcast(self, message: str):
        print(f"Broadcasting message: '{message}' to {len(self.active_connections)} clients")
        tasks = [conn.send_text(message) for conn in self.active_connections]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"Error broadcasting message: {result}")



manager = ConnectionManager()
router = APIRouter( prefix="/ws",tags=["WebSockets"] )

@router.websocket("/chat/{client_id}")
async def ws_chat(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined the chat")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {client_id}: {data}")
            await manager.broadcast(f"Client #{client_id}: {data}")

    except WebSocketDisconnect:
        await manager.close(websocket)

    except Exception as e:
        print(f"Error for client #{client_id}: {e}")
        await manager.close(websocket)
    
