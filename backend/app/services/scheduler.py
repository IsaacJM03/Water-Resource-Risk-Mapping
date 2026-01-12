from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.water_source import WaterSource
from app.models.risk_history import RiskHistory
from app.services.risk_engine import calculate_risk
from app.utils.logger import logger
from app.services.alerts import evaluate_alert
from app.services.environment_simulator import (
    simulate_rainfall,
    simulate_water_level
)
from app.services.trends import calculate_trend

def recalculate_risks():
    db: Session = SessionLocal()
    sources = db.query(WaterSource).all()
    
    # query historical risk
    recent = (
        db.query(RiskHistory.risk_score)
        .filter(RiskHistory.water_source_id == source.id)
        .order_by(RiskHistory.created_at.desc())
        .limit(5)
        .all()
    )

    recent_scores = [r[0] for r in recent]
    trend = calculate_trend(recent_scores)

    for source in sources:
        source.rainfall = simulate_rainfall(source.rainfall)
        source.water_level = simulate_water_level(source.water_level)

        risk = calculate_risk(source.rainfall, source.water_level)

        history = RiskHistory(
            water_source_id=source.id,
            risk_score=risk
        )

        db.add(history)
        logger.info(f"Recalculated risk for source {source.id}: {risk}")

    db.commit()
    db.close()
    evaluate_alert(risk, source.name)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(recalculate_risks, "interval", hours=24)
    scheduler.start()