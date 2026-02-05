from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PushTokenRegister(BaseModel):
    token: str = Field(..., description="Expo push token")

class PushTokenResponse(BaseModel):
    message: str
    user_id: int
    token: str

class PushNotificationCreate(BaseModel):
    title: str
    body: str
    data: Optional[dict] = None

class PushNotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    status: str
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True