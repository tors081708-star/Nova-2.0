"""
NOVA Web Dashboard Server.
FastAPI + WebSocket streaming for real-time agent monitoring and To-Do task management endpoints.
"""

import os
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from nova.agents.core.nova_mind import NovaMind

app = FastAPI(title="NOVA 2.0 Agent Dashboard")

mind = NovaMind()

class TaskCreate(BaseModel):
    title: str
    category: Optional[str] = "general"

class QueryRequest(BaseModel):
    query: str

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/api/tasks")
def get_tasks():
    return [t.to_dict() for t in mind.get_all_tasks()]

@app.post("/api/tasks")
def create_task(task_data: TaskCreate):
    task = mind.add_task(title=task_data.title, category=task_data.category)
    return task.to_dict()

@app.post("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: str):
    task = mind.toggle_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    success = mind.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "deleted", "id": task_id}

@app.post("/api/query")
def process_query(req: QueryRequest):
    res = mind.process_query(req.query)
    return res

@app.websocket("/ws/monitor")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json({"status": "connected", "agent": "NOVA 2.0", "autonomy": mind.user_profile.autonomy})
        while True:
            data = await websocket.receive_text()
            response = mind.process_query(data)
            await websocket.send_json(response)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Serve static files if public directory exists
public_dir = os.path.join(os.path.dirname(__file__), "public")
if os.path.exists(public_dir):
    app.mount("/static", StaticFiles(directory=public_dir), name="static")

    @app.get("/")
    def read_root():
        index_file = os.path.join(public_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "NOVA 2.0 Web Dashboard API"}
