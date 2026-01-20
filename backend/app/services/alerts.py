from app.utils.logger import get_logger
from sqlalchemy.orm import Session
from app.models.alert import Alert

logger = get_logger()

CRITICAL_RISK_THRESHOLD = 80


def evaluate_alert(risk_score: int) -> bool:
    """
    PURE FUNCTION
    Determines whether an alert should be considered
    """
    return risk_score >= CRITICAL_RISK_THRESHOLD




def create_or_update_alert(
    db: Session,
    source,
    risk_score: int,
    level: str
):
    """
    SIDE-EFFECT FUNCTION
    Creates or updates alerts in the DB
    """

    existing = (
        db.query(Alert)
        .filter(
            Alert.water_source_id == source.id,
            Alert.organization_id == source.organization_id,
            Alert.acknowledged == False
        )
        .order_by(Alert.created_at.desc())
        .first()
    )

    if existing:
        # Do not spam duplicate alerts
        return existing

    alert = Alert(
        water_source_id=source.id,
        organization_id=source.organization_id,
        level=level,
        message=f"Risk level is {level.upper()} ({risk_score}%)"
    )

    db.add(alert)
    db.commit()

    logger.warning(
        f"ALERT CREATED: source={source.id}, org={source.organization_id}, level={level}"
    )

    return alert
