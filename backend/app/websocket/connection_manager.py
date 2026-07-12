from collections import defaultdict

from fastapi import WebSocket

from app.core.logger import logger


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(
        self,
        session_id: str,
        websocket: WebSocket,
    ) -> None:
        await websocket.accept()

        self.connections[session_id].append(websocket)

        logger.info(
            "WebSocket connected | session=%s clients=%d",
            session_id,
            len(self.connections[session_id]),
        )

    def disconnect(
        self,
        session_id: str,
        websocket: WebSocket,
    ) -> None:
        if session_id not in self.connections:
            return

        if websocket in self.connections[session_id]:
            self.connections[session_id].remove(websocket)

        if not self.connections[session_id]:
            del self.connections[session_id]

        logger.info(
            "WebSocket disconnected | session=%s clients=%d",
            session_id,
            len(self.connections.get(session_id, [])),
        )

    async def send(
        self,
        session_id: str,
        message: dict,
    ) -> None:
        for websocket in list(self.connections.get(session_id, [])):
            try:
                await websocket.send_json(message)
            except Exception:
                logger.exception(
                    "Failed to send WebSocket message."
                )
                self.disconnect(session_id, websocket)


connection_manager = ConnectionManager()