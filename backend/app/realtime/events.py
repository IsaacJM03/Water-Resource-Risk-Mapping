from enum import Enum


class EventType(str, Enum):
    RISK_UPDATE = "risk_update"
    FORECAST_UPDATE = "forecast_update"
    ALERT_TRIGGERED = "alert_triggered"
