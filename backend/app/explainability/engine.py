from app.explainability.rules import explain_factors
from app.explainability.narratives import generate_summary
from app.explainability.schemas import RiskExplanation


def explain_risk(source, risk_score, trend):
    primary, factors = explain_factors(
        source.rainfall,
        source.water_level,
        trend
    )

    summary = generate_summary(risk_score, primary, trend)

    return RiskExplanation(
        risk_score=risk_score,
        primary_driver=primary,
        contributors=factors,
        trend=trend,
        summary=summary
    )
