import pandas as pd

def build_dataset(risk_history):
    """
    Converts DB rows into ML-ready dataframe
    """
    return pd.DataFrame(
        [{
            "timestamp": r.created_at,
            "risk": r.risk_score
        } for r in risk_history]
    ).sort_values("timestamp")