# from ..schemas.water_source import WaterSourceRead


# def compute_risk_score(source: WaterSourceRead) -> float:
#     """Placeholder risk calculation combining capacity and quality."""
#     return max(0.0, min(1.0, (source.quality_index / 100.0) * 0.7 + (source.capacity / 1000.0) * 0.3))

def calculate_risk(rainfall: float, water_level: float) -> int:
    risk = 0

    if rainfall < 50:
        risk += 40
    if water_level < 20:
        risk += 60

    return min(risk, 100)
