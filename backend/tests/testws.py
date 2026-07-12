import asyncio
import websockets

async def main():
    async with websockets.connect(
        "ws://localhost:8000/ws/string"
    ) as ws:
        print("Connected!")

        while True:
            msg = await ws.recv()
            print(msg)

asyncio.run(main())