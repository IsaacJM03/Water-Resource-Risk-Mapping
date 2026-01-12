from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.water_source import WaterSource
from app.models.risk_history import RiskHistory
from app.services.risk_engine import calculate_risk
from app.utils.logger import logger

def recalculate_risks():
    db: Session = SessionLocal()
    sources = db.query(WaterSource).all()

    for source in sources:
        risk = calculate_risk(source.rainfall, source.water_level)

        history = RiskHistory(
            water_source_id=source.id,
            risk_score=risk
        )

        db.add(history)
        logger.info(f"Recalculated risk for source {source.id}: {risk}")

    db.commit()
    db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(recalculate_risks, "interval", hours=24)
    scheduler.start()