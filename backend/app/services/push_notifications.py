import requests
import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User, PushNotification
from app.core.config import get_settings
from app.utils.logger import get_logger

logger = get_logger()
settings = get_settings()

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

class PushNotificationService:
    """Service for sending push notifications via Expo"""

    @staticmethod
    def validate_token(token: str) -> bool:
        """Validate Expo push token format"""
        return token.startswith("ExponentPushToken[") and token.endswith("]")

    @staticmethod
    def send_push_notification(
        token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        priority: str = "high",
        sound: str = "default"
    ) -> Dict[str, Any]:
        """
        Send a push notification to a single device
        
        Args:
            token: Expo push token
            title: Notification title
            body: Notification body
            data: Optional extra data
            priority: high or normal
            sound: default or null
        
        Returns:
            Response from Expo push service
        """
        if not PushNotificationService.validate_token(token):
            logger.error(f"Invalid Expo push token: {token}")
            return {"status": "error", "message": "Invalid token format"}

        payload = {
            "to": token,
            "title": title,
            "body": body,
            "sound": sound,
            "priority": priority,
        }

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                EXPO_PUSH_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Push notification sent successfully: {result}")
            return result
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    def send_batch_notifications(
        tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Send push notifications to multiple devices"""
        messages = [
            {
                "to": token,
                "title": title,
                "body": body,
                "sound": "default",
                "priority": "high",
                "data": data or {}
            }
            for token in tokens
            if PushNotificationService.validate_token(token)
        ]

        if not messages:
            return []

        try:
            response = requests.post(
                EXPO_PUSH_URL,
                json=messages,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send batch notifications: {str(e)}")
            return []

    @staticmethod
    def send_alert_notification(
        db: Session,
        alert_id: int,
        source_name: str,
        risk_score: float,
        level: str
    ):
        """Send push notification for a critical alert"""
        # Get all users with push tokens enabled
        users = db.query(User).filter(
            User.expo_push_token.isnot(None),
            User.push_notifications_enabled == True
        ).all()

        if not users:
            logger.warning("No users with push tokens found")
            return

        # Create notification message
        emoji = "🔴" if level == "critical" else "🟠" if level == "high" else "🟡"
        title = f"{emoji} Water Risk Alert"
        body = f"{source_name} risk is {level.upper()} ({risk_score:.1f}%)"
        
        data = {
            "type": "alert",
            "alert_id": alert_id,
            "source_name": source_name,
            "risk_score": risk_score,
            "level": level,
        }

        # Send to all users
        for user in users:
            try:
                result = PushNotificationService.send_push_notification(
                    token=user.expo_push_token,
                    title=title,
                    body=body,
                    data=data
                )

                # Store notification record
                notification = PushNotification(
                    user_id=user.id,
                    alert_id=alert_id,
                    title=title,
                    body=body,
                    data=json.dumps(data),
                    status="sent" if result.get("data", {}).get("status") == "ok" else "failed",
                    expo_ticket_id=result.get("data", {}).get("id"),
                )
                db.add(notification)
            
            except Exception as e:
                logger.error(f"Failed to send notification to user {user.id}: {str(e)}")

        db.commit()