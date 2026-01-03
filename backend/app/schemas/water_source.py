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
