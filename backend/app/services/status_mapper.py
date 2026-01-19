def map_status(risk: float):
    if risk >= 80:
        return "critical"
    elif risk >= 60:
        return "high"
    elif risk >= 30:
        return "moderate"
    return "safe"
