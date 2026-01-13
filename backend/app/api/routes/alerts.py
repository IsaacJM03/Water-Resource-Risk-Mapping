from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/alerts")

@router.get("/")
def list_alerts(db=Depends(get_db)):
    return (
        db.query(Alert)
        .filter(Alert.acknowledged == False)
        .order_by(Alert.created_at.desc())
        .all()
    )

@router.post("/{alert_id}/ack")
def acknowledge_alert(alert_id: int, db=Depends(get_db)):
    alert = db.query(Alert).get(alert_id)
    alert.acknowledged = True
    db.commit()
    return {"status": "acknowledged"}