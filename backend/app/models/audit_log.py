import datetime
from sqlalchemy import Column, DateTime, Integer, String
from backend.app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String(255))
    actor = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)