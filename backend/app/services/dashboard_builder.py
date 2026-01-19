from app.services.status_mapper import map_status
from app.services.trends import calculate_trend
from app.ml.predictor import forecast_risk
from app.models.risk_history import RiskHistory


def build_source_dashboard(source, db):
    history = (
        db.query(RiskHistory)
        .filter(RiskHistory.water_source_id == source.id)
        .order_by(RiskHistory.created_at)
        .all()
    )

    recent_scores = [h.risk_score for h in history[-5:]]
    trend = calculate_trend(recent_scores)
    forecast = forecast_risk(history)

    return {
        "id": source.id,
        "name": source.name,
        "risk_score": round(source.risk_score, 1),
        "trend": trend,
        "forecast": round(forecast, 1) if forecast else None,
        "status": map_status(source.risk_score)
    }
