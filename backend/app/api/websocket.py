from app.websocket.connection_manager import connection_manager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
):
    await connection_manager.connect(
        session_id,
        websocket,
    )

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(
            session_id,
            websocket,
        )
