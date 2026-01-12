def calculate_trend(risks: list[float]):
    if len(risks) < 3:
        return "stable"

    delta = risks[-1] - risks[-3]

    if delta > 10:
        return "rising"
    if delta < -10:
        return "falling"
    return "stable"

def forecast_next_risk(risks):
    if len(risks) < 2:
        return risks[-1]
    return min(100, risks[-1] + (risks[-1] - risks[-2]))