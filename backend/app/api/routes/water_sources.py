from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.water_source import WaterSource
from app.schemas.water_source import WaterSourceCreate, WaterSourceOut
from app.services.risk_engine import calculate_risk
from app.models.risk_history import RiskHistory
from app.auth.dependencies import get_current_context

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=WaterSourceOut)
def create_water_source(payload: WaterSourceCreate, db: Session = Depends(get_db)):
    risk_score = calculate_risk(payload.rainfall, payload.water_level)
    source = WaterSource(**payload.dict())
    db.add(source)
    db.commit()
    db.refresh(source)
    history = RiskHistory(
        water_source_id=source.id,
        risk_score=risk_score
    )
    db.add(history)
    db.commit()

    db.refresh(source)

    return source

# @router.get("/")
# def list_sources(org_id: int, db: Session = Depends(get_db)):
#     sources = db.query(WaterSource).filter(WaterSource.organization_id == org_id).all()
#     results = []

#     for source in sources:
#         latest = (
#             db.query(RiskHistory)
#             .filter(RiskHistory.water_source_id == source.id)
#             .order_by(RiskHistory.recorded_at.desc())
#             .first()
#         )

#         results.append({
#             "id": source.id,
#             "name": source.name,
#             "latitude": source.latitude,
#             "longitude": source.longitude,
#             "risk_score": latest.risk_score if latest else None
#         })

#     return results

@router.get("/{source_id}/risk-history")
def risk_history(source_id: int, org_id: int, db: Session = Depends(get_db)):
    history = (
        db.query(RiskHistory)
        .filter(RiskHistory.water_source_id == source_id)
        .order_by(RiskHistory.recorded_at.asc())
        .filter(
            WaterSource.organization_id == org_id
        ).all()
    )

    return [
        {
            "risk_score": h.risk_score,
            "recorded_at": h.recorded_at
        }
        for h in history
    ]

@router.get("/")
def list_sources(
    context = Depends(get_current_context),
    db: Session = Depends(get_db)
):
    org_id = context["organization_id"]

    return db.query(WaterSource).filter(
        WaterSource.organization_id == org_id
    ).all()