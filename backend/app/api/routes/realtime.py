from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.realtime.broadcaster import manager

router = APIRouter()


@router.websocket("/ws/risk")
async def risk_updates(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            # keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
