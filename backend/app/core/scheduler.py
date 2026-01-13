from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.water_source import WaterSource
from app.models.risk_history import RiskHistory
from app.services.risk_engine import calculate_risk
from app.utils.logger import get_logger
from app.services.alerts import evaluate_alert
from app.models.alert import Alert
from app.services.alert_engine import (
    determine_alert_level,
    should_trigger_alert
)
from app.ml.predictor import forecast_risk



logger = get_logger()
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
    
    level = determine_alert_level(risk)

    # add alerts
    if level:
        existing = (
            db.query(Alert)
            .filter(
                Alert.water_source_id == source.id,
                Alert.acknowledged == False
            )
            .order_by(Alert.created_at.desc())
            .first()
        )

        if should_trigger_alert(existing, level):
            alert = Alert(
                water_source_id=source.id,
                level=level,
                message=f"Risk level is {level.upper()} ({risk})"
            )
            db.add(alert)
            
        history = (
            db.query(RiskHistory)
            .filter(RiskHistory.water_source_id == source.id)
            .order_by(RiskHistory.created_at)
            .all()
        )

        forecast = forecast_risk(history)

        if forecast and forecast >= 80:
            logger.warning(
                f"Forecasted CRITICAL risk for source {source.id}: {forecast}"
            )

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(recalculate_risks, "interval", hours=24)
    scheduler.start()