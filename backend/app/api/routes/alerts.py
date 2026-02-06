from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.alert import Alert
from app.models.water_source import WaterSource
from app.models.user import User
from app.api.deps import get_current_user
from app.services.push_notifications import PushNotificationService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Pydantic schemas for request/response
class AlertCreate(BaseModel):
    water_source_id: int
    level: str  # low, medium, high, critical
    message: str

class AlertResponse(BaseModel):
    id: int
    water_source_id: int
    level: str
    message: str
    acknowledged: bool
    organization_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AlertAcknowledge(BaseModel):
    acknowledged: bool = True

@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all alerts for current user's organization"""
    alerts = (
        db.query(Alert)
        .filter(Alert.organization_id == current_user.organization_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return alerts

@router.get("/unacknowledged", response_model=List[AlertResponse])
def get_unacknowledged_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get unacknowledged alerts"""
    alerts = (
        db.query(Alert)
        .filter(
            Alert.organization_id == current_user.organization_id,
            Alert.acknowledged == False
        )
        .all()
    )
    return alerts

@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new alert and send push notifications if critical"""
    # Verify water source exists and belongs to organization
    source = (
        db.query(WaterSource)
        .filter(
            WaterSource.id == alert.water_source_id,
            WaterSource.organization_id == current_user.organization_id
        )
        .first()
    )
    
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Water source not found or access denied"
        )

    # Create alert
    db_alert = Alert(
        water_source_id=alert.water_source_id,
        level=alert.level.lower(),
        message=alert.message,
        organization_id=current_user.organization_id,
        acknowledged=False
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)

    # Send push notification if critical or high
    if alert.level.lower() in ["critical", "high"]:
        try:
            # Calculate risk score from water source data
            risk_score = calculate_risk_score(source)
            
            PushNotificationService.send_alert_notification(
                db=db,
                alert_id=db_alert.id,
                source_name=source.name,
                risk_score=risk_score,
                level=alert.level.lower()
            )
        except Exception as e:
            # Log but don't fail the alert creation
            print(f"Failed to send push notification: {e}")

    return db_alert

@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark an alert as acknowledged"""
    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.organization_id == current_user.organization_id
        )
        .first()
    )
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found or access denied"
        )
    
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    
    return alert

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an alert (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    alert = (
        db.query(Alert)
        .filter(
            Alert.id == alert_id,
            Alert.organization_id == current_user.organization_id
        )
        .first()
    )
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found or access denied"
        )
    
    db.delete(alert)
    db.commit()
    
    return None

def calculate_risk_score(source: WaterSource) -> float:
    """Calculate risk score from water source data"""
    # Use your existing risk calculation logic
    rainfall_score = max(0, 100 - source.rainfall) if source.rainfall else 50
    water_level_score = max(0, 100 - source.water_level) if source.water_level else 50
    
    risk_score = (rainfall_score * 0.6) + (water_level_score * 0.4)
    return min(100, max(0, risk_score))