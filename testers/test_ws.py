import asyncio

import websockets


async def hello():
    uri = "ws://localhost:8000/ws/group1/client1"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, Server!")
        response = await websocket.recv()
        print(f"Received message from server: {response}")


asyncio.run(hello())
