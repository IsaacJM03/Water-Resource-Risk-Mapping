from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer")  # viewer, admin, analyst
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    expo_push_token = Column(String, nullable=True)  # Store Expo push token
    push_notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class PushNotification(Base):
    __tablename__ = "push_notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    data = Column(String, nullable=True)  # JSON string for extra data
    status = Column(String, default="pending")  # pending, sent, failed
    expo_ticket_id = Column(String, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())