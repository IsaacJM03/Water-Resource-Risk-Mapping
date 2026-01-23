from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.water_source import WaterSource

router = APIRouter()

@router.get("/")
def list_sources(limit: int = 10, offset: int = 0, db=Depends(get_db)):
    return db.query(WaterSource).limit(limit).offset(offset).all()

@router.get("/{source_id}")
def get_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(WaterSource).filter(WaterSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Water source not found")
    return source