from fastapi import APIRouter, Depends
from app.models.risk_history import RiskHistory
from app.api.water_sources import get_db
from app.ml.predictor import forecast_risk
from app.services.trends import calculate_trend

router = APIRouter()


@router.get("/trends/{source_id}")
def get_trends(source_id: int, db=Depends(get_db)):
    history = (
        db.query(RiskHistory)
        .filter(RiskHistory.water_source_id == source_id)
        .order_by(RiskHistory.created_at)
        .all()
    )

    risks = [h.risk_score for h in history]
    return {
        "trend": calculate_trend(risks),
        "history": risks
    }
    
@router.get("/forecast/{source_id}")
def forecast(source_id: int, db=Depends(get_db)):
    history = (
        db.query(RiskHistory)
        .filter(RiskHistory.water_source_id == source_id)
        .order_by(RiskHistory.recorded_at)
        .all()
    )

    forecast = forecast_risk(history)

    return {
        "source_id": source_id,
        "forecasted_risk": forecast
    }