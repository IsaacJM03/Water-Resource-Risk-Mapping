from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

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

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from OAuth2 token"""
    if not token:
        # Return default user for development
        user = db.query(User).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No users found in database"
            )
        return user
    
    # Decode JWT and get user
    # TODO: Implement JWT decoding
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user