from fastapi import FastAPI, status, HTTPException, WebSocket, WebSocketDisconnect
from typing import Optional, List
from pydantic import BaseModel
from routers import sessionManagement
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(sessionManagement.router)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def activate(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disactivate(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message:str):
        for ws in self.active_connections:
            await ws.send_text(message)
connectionManager = ConnectionManager()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "script is running "}

@app.websocket("/ws/")
async def websocket_channel(websocket: WebSocket):
    await connectionManager.activate(websocket)
    try:
        while True:
            recieved = await websocket.receive_text()
            print(recieved)
            await connectionManager.broadcast(recieved)
    except WebSocketDisconnect:
        connectionManager.disactivate(websocket)
        await connectionManager.broadcast("Client left the channel")

