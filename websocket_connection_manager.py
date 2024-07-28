import asyncio
from fastapi import WebSocket


class WebSocketConnectionManager:
    def __init__(self) -> None:
        self.__active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.__active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.__active_connections.remove(ws)

    async def broadcast(self, msg: str):
        await asyncio.gather(
            *[conn.send_text(msg) for conn in self.__active_connections]
        )