from typing import Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class Client:
    def __init__(self, group: str, name: str, websocket: WebSocket):
        self.client_group = group
        self.client_name = name
        self.action_data: Dict[str, Optional[str]] = {}
        self.client_ws = websocket

    async def send_text(self, data: str):
        await self.client_ws.send_text(data)

    async def receive_text(self) -> str:
        return await self.client_ws.receive_text()


app = FastAPI()
clients: Dict[str, Client] = {}


@app.websocket("/ws/{client_group}/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_group: str, client_name: str):
    await websocket.accept()
    client = Client(client_group, client_name, websocket)
    clients[f"{client_group}->{client_name}"] = client

    try:
        while True:
            data = await client.receive_text()
            print(f"Received data '{data}' from client {client_name} in group {client_group}")
            await client.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        clients.pop(f"{client_group}->{client_name}")
        print(f"Client {client_name} in group {client_group} disconnected")


@app.get("/clients")
def get_clients():
    return {"clients": list(clients.keys())}
