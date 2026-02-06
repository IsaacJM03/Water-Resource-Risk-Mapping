from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from datetime import datetime
from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    water_source_id = Column(Integer, ForeignKey("water_sources.id"))
    level = Column(String(20))  # low, medium, high, critical
    message = Column(String(255))
    acknowledged = Column(Boolean, default=False)
    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=func.now())