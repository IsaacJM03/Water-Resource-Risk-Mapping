from app.realtime.manager import ConnectionManager
from app.realtime.events import EventType

manager = ConnectionManager()


async def broadcast_risk_update(source_id: int, payload: dict):
    await manager.broadcast({
        "type": EventType.RISK_UPDATE,
        "source_id": source_id,
        "data": payload
    })
