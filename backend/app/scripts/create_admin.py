from app.core.database import SessionLocal
from app.models.user import User
from app.services.auth import hash_password

db = SessionLocal()

admin = User(
    email="admin@example.com",
    hashed_password=hash_password("admin123"),
    role="admin"
)

db.add(admin)
db.commit()
db.close()