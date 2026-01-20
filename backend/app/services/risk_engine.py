from app.realtime.broadcaster import broadcast_risk_update
from app.services.dashboard_builder import build_source_dashboard
from app.explainability.engine import explain_risk
from app.services.trends import calculate_trend
from app.services.alerts import evaluate_alert, create_or_update_alert
from app.services.alert_engine import determine_alert_level


def calculate_risk(rainfall: float, water_level: float) -> int:
    """
    PURE FUNCTION
    No DB
    No side effects
    """
    risk = 0

    if rainfall < 50:
        risk += 40
    if water_level < 20:
        risk += 60

    return min(risk, 100)


async def update_risk(source, new_score: int, db):
    """
    ORCHESTRATION FUNCTION
    Coordinates everything AFTER risk changes
    """

    # 1️⃣ Persist risk
    source.risk_score = new_score
    db.commit()

    # 2️⃣ Calculate trend (from history)
    recent_scores = [
        r.risk_score for r in source.risk_history[-5:]
    ]
    trend = calculate_trend(recent_scores)

    # 3️⃣ Generate explanation (THIS IS STEP 6)
    explanation = explain_risk(
        source=source,
        risk_score=new_score,
        trend=trend
    )


    if evaluate_alert(new_score):
        level = determine_alert_level(new_score)

        create_or_update_alert(
            db=db,
            source=source,
            risk_score=new_score,
            level=level
        )

    # (optional) persist explanation later
    # db.add(RiskExplanationModel(...))

    # 4️⃣ Build dashboard payload
    payload = build_source_dashboard(source, db)
    payload["explanation"] = explanation.dict()

    # 5️⃣ Broadcast realtime update
    await broadcast_risk_update(source.id, payload)
