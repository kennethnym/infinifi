import asyncio
from websockets.server import serve

from generate import generate


async def handler(websocket):
    async for message in websocket:
        if message != "generate":
            continue

        print("generating new audio clips...")

        generate()

        print("audio generated")

        for i in range(5):
            with open(f"{i}.mp3", "rb") as f:
                data = f.read()
                await websocket.send(data)


async def main():
    async with serve(handler, "localhost", 8001, ping_interval=5):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
