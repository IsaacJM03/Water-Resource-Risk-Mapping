from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class WaterSource(Base):
    __tablename__ = "water_sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    water_level = Column(Float)
    rainfall = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
