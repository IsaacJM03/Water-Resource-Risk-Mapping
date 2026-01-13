from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.models.water_source import WaterSource

router = APIRouter(prefix="/sources")

@router.get("/")
def list_sources(limit: int = 10, offset: int = 0, db=Depends(get_db)):
    return db.query(WaterSource).limit(limit).offset(offset).all()