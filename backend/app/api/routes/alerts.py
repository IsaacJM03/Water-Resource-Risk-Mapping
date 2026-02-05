from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app.core.database import get_db
from app.models.alert import Alert
from app.models.water_source import WaterSource
from app.models.risk_history import RiskHistory
from app.services.risk_engine import calculate_risk
from app.api.deps import get_current_user, require_roles
from backend.app.models.user import User

router = APIRouter(prefix="/alerts")

@router.get("/")
def list_alerts(db=Depends(get_db)):
    """List all unacknowledged alerts, sorted by most recent."""
    return (
        db.query(Alert)
        .filter(Alert.acknowledged == False)
        .order_by(Alert.created_at.desc())
        .all()
    )

@router.post("/{alert_id}/ack")
def acknowledge_alert(alert_id: int, db=Depends(get_db)):
    """Acknowledge a specific alert by ID."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    alert.acknowledged = True
    db.commit()
    return {"status": "acknowledged"}

@router.get("/forecast/{source_id}")
def forecast(source_id: int, db=Depends(get_db)):
    """Forecast future risk and potential alerts for a water source."""
    # Get water source
    source = db.query(WaterSource).filter(WaterSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Water source {source_id} not found")
    
    # Get historical risk data
    history = (
        db.query(RiskHistory)
        .filter(RiskHistory.water_source_id == source_id)
        .order_by(RiskHistory.recorded_at.asc())
        .all()
    )
    
    if not history:
        return {
            "source_id": source_id,
            "forecasted_risk": 0,
            "alert_level": "low",
            "potential_alerts": []
        }
    
    # Calculate average trend
    recent_risks = [h.risk_score for h in history[-10:]]  # Last 10 records
    current_risk = recent_risks[-1] if recent_risks else 0
    avg_risk = sum(recent_risks) / len(recent_risks) if recent_risks else 0
    
    # Simple forecast: assume trend continues
    trend = current_risk - avg_risk
    forecasted_risk = min(100, max(0, current_risk + trend))
    
    # Determine alert level
    if forecasted_risk >= 80:
        alert_level = "critical"
    elif forecasted_risk >= 60:
        alert_level = "high"
    elif forecasted_risk >= 40:
        alert_level = "medium"
    else:
        alert_level = "low"
    
    # Generate potential alerts if risk is elevated
    potential_alerts = []
    if forecasted_risk >= 40:
        if source.water_level and source.water_level < 20:
            potential_alerts.append({
                "type": "low_water_level",
                "message": f"Water level {source.water_level}m is below safety threshold",
                "severity": "high"
            })
        if source.rainfall and source.rainfall < 50:
            potential_alerts.append({
                "type": "low_rainfall",
                "message": f"Rainfall {source.rainfall}mm is insufficient",
                "severity": "medium"
            })
    
    return {
        "source_id": source_id,
        "source_name": source.name,
        "current_risk": current_risk,
        "forecasted_risk": round(forecasted_risk, 2),
        "trend": round(trend, 2),
        "alert_level": alert_level,
        "potential_alerts": potential_alerts
    }


@router.get(
    "/forecast/{source_id}",
    dependencies=[
        Depends(require_roles("admin", "analyst", "viewer"))
    ]
)
def forecast(source_id: int, db=Depends(get_db)):
    ...

from app.services.push_notifications import PushNotificationService

@router.post("/", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new alert and send push notifications if critical"""
    # Get water source
    source = db.query(WaterSource).filter(WaterSource.id == alert.water_source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Water source not found")

    # Create alert
    db_alert = Alert(
        water_source_id=alert.water_source_id,
        level=alert.level,
        message=alert.message,
        organization_id=current_user.organization_id,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)

    # Send push notification if critical or high
    if alert.level in ["critical", "high"]:
        risk_score = source.risk_score or 0
        PushNotificationService.send_alert_notification(
            db=db,
            alert_id=db_alert.id,
            source_name=source.name,
            risk_score=risk_score,
            level=alert.level
        )

    return db_alert