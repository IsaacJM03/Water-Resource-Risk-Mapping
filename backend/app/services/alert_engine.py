def determine_alert_level(risk_score: float):
    if risk_score >= 85:
        return "critical"
    if risk_score >= 65:
        return "high"
    if risk_score >= 40:
        return "medium"
    return None

def should_trigger_alert(existing_alert, new_level):
    if not existing_alert:
        return True
    if existing_alert.acknowledged:
        return True
    return existing_alert.level != new_level