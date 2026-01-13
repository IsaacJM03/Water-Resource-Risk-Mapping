from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.water_source import WaterSource
from app.models.risk_history import RiskHistory
from app.models.alert import Alert

from app.services.risk_engine import calculate_risk
from app.services.environment_simulator import (
    simulate_rainfall,
    simulate_water_level
)
from app.services.trends import calculate_trend
from app.services.alert_engine import (
    determine_alert_level,
    should_trigger_alert
)

from app.ml.predictor import forecast_risk
from app.utils.logger import get_logger

logger = get_logger()


def recalculate_risks():
    db: Session = SessionLocal()

    try:
        sources = db.query(WaterSource).all()

        for source in sources:
            # --- simulate environment ---
            source.rainfall = simulate_rainfall(source.rainfall)
            source.water_level = simulate_water_level(source.water_level)

            # --- calculate risk ---
            risk = calculate_risk(
                source.rainfall,
                source.water_level
            )

            # --- store history ---
            db.add(RiskHistory(
                water_source_id=source.id,
                risk_score=risk
            ))

            logger.info(
                f"Source {source.id} risk recalculated: {risk}"
            )

            # --- trend analysis ---
            recent = (
                db.query(RiskHistory.risk_score)
                .filter(RiskHistory.water_source_id == source.id)
                .order_by(RiskHistory.created_at.desc())
                .limit(5)
                .all()
            )
            recent_scores = [r[0] for r in recent]
            trend = calculate_trend(recent_scores)

            # --- alerting ---
            level = determine_alert_level(risk)
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
                    db.add(Alert(
                        water_source_id=source.id,
                        level=level,
                        message=f"Risk is {level.upper()} ({risk})"
                    ))

            # --- forecasting ---
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

        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Scheduler failed: {e}")

    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(recalculate_risks, "interval", hours=24)
    scheduler.start()