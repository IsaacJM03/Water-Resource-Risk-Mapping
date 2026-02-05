from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.user import User, PushNotification
from app.schemas.push_tokens import (
    PushTokenRegister,
    PushTokenResponse,
    PushNotificationResponse,
)
from app.services.push_notifications import PushNotificationService


router = APIRouter(prefix="/push", tags=["push-notifications"])

@router.post("/register", response_model=PushTokenResponse)
def register_push_token(
    payload: PushTokenRegister,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register or update a user's Expo push token
    """
    if not PushNotificationService.validate_token(payload.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Expo push token format"
        )

    # Update user's push token
    current_user.expo_push_token = payload.token
    current_user.push_notifications_enabled = True
    db.commit()

    return PushTokenResponse(
        message="Push token registered successfully",
        user_id=current_user.id,
        token=payload.token
    )

@router.delete("/unregister")
def unregister_push_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove user's push token and disable notifications"""
    current_user.expo_push_token = None
    current_user.push_notifications_enabled = False
    db.commit()

    return {"message": "Push notifications disabled successfully"}

@router.post("/toggle")
def toggle_push_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle push notifications on/off"""
    current_user.push_notifications_enabled = not current_user.push_notifications_enabled
    db.commit()

    return {
        "message": "Push notifications updated",
        "enabled": current_user.push_notifications_enabled
    }

@router.get("/history", response_model=List[PushNotificationResponse])
def get_notification_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's push notification history"""
    notifications = (
        db.query(PushNotification)
        .filter(PushNotification.user_id == current_user.id)
        .order_by(PushNotification.created_at.desc())
        .limit(limit)
        .all()
    )
    return notifications

@router.post("/test")
def send_test_notification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a test push notification to current user"""
    if not current_user.expo_push_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No push token registered"
        )

    result = PushNotificationService.send_push_notification(
        token=current_user.expo_push_token,
        title="🧪 Test Notification",
        body="This is a test notification from Water Risk Monitor",
        data={"type": "test"}
    )

    return {
        "message": "Test notification sent",
        "result": result
    }


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