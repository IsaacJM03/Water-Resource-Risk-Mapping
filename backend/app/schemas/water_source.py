from pydantic import BaseModel

class WaterSourceCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    water_level: float
    rainfall: float

class WaterSourceOut(WaterSourceCreate):
    id: int

    class Config:
        orm_mode = True

class WaterSourceDashboard(BaseModel):
    id: int
    name: str
    risk_score: float
    trend: str
    forecast: float | None
    status: str