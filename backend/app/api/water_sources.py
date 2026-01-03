from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.water_source import WaterSource
from app.schemas.water_source import WaterSourceCreate, WaterSourceOut
from app.services.risk_engine import calculate_risk

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=WaterSourceOut)
def create_water_source(payload: WaterSourceCreate, db: Session = Depends(get_db)):
    risk = calculate_risk(payload.rainfall, payload.water_level)

    source = WaterSource(**payload.dict())
    db.add(source)
    db.commit()
    db.refresh(source)

    return source
