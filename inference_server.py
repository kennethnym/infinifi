import asyncio
from websockets.server import serve

from generate import generate
from logger import log_info


async def handler(websocket):
    async for message in websocket:
        if message != "generate":
            continue

        log_info("generating new audio clips...")

        generate()

        log_info("audio generated")

        for i in range(5):
            with open(f"{i}.mp3", "rb") as f:
                data = f.read()
                await websocket.send(data)


async def main():
    async with serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
