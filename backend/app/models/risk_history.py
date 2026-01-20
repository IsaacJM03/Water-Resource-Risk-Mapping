from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class RiskHistory(Base):
    __tablename__ = "risk_history"

    id = Column(Integer, primary_key=True)
    water_source_id = Column(Integer, ForeignKey("water_sources.id"))
    risk_score = Column(Integer)
    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )
    recorded_at = Column(DateTime, default=datetime.utcnow)
