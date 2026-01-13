from app.ml.dataset import build_dataset
from app.ml.model import RiskForecastModel

def forecast_risk(risk_history):
    if len(risk_history) < 5:
        return None

    df = build_dataset(risk_history)
    risks = df["risk"].values

    model = RiskForecastModel()
    model.train(risks)

    return model.predict_next()