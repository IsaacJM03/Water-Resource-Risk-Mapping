from app.utils.logger import get_logger

logger = get_logger()
CRITICAL_RISK_THRESHOLD = 80

def evaluate_alert(risk_score, source_name):
    if risk_score >= CRITICAL_RISK_THRESHOLD:
        logger.warning(
            f"CRITICAL ALERT: {source_name} risk at {risk_score}%"
        )
        return True
    return False