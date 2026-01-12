from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta

SECRET = "change-me"
ALGORITHM = "HS256"

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=8)
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def require_role(user, allowed):
    if user.role not in allowed:
        raise HTTPException(status_code=403)