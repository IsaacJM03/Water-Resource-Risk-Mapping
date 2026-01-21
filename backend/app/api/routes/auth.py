from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form.username
    ).first()

    if not user or not verify_password(
        form.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"user_id": user.id}
    )

    return {"access_token": token, "token_type": "bearer"}
