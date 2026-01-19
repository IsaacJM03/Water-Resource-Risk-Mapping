def classify_impact(weight: float) -> str:
    if weight >= 0.6:
        return "high"
    if weight >= 0.3:
        return "medium"
    return "low"


def explain_factors(rainfall, water_level, trend):
    factors = []

    rainfall_weight = 0.55
    water_level_weight = 0.45

    factors.append({
        "factor": "rainfall",
        "value": rainfall,
        "weight": rainfall_weight,
        "impact": classify_impact(rainfall_weight)
    })

    factors.append({
        "factor": "water_level",
        "value": water_level,
        "weight": water_level_weight,
        "impact": classify_impact(water_level_weight)
    })

    primary = "rainfall" if rainfall_weight > water_level_weight else "water_level"

    return primary, factors
