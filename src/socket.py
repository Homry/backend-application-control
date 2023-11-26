from typing import List
from fastapi import WebSocket


class Socket:
    def __init__(self):
        self.__active_connection: List[WebSocket] = []

    def add_connection(self, ws: WebSocket) -> None:
        self.__active_connection.append(ws)

    async def send_message(self, app: str) -> None:
        for connection in self.__active_connection:
            await connection.send_text(app)

    def remove_connection(self, socket: WebSocket) -> None:
        self.__active_connection.remove(socket)
