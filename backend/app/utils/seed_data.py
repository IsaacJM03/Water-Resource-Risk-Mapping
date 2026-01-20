from app.core.database import SessionLocal
from app.models.organization import Organization
from app.models.user import User
from app.models.membership import Membership
from app.models.water_source import WaterSource
from app.models.risk_history import RiskHistory
from app.services.risk_engine import calculate_risk
from app.services.auth import hash_password


def seed():
    db = SessionLocal()
    try:
        # 1) Organization
        org = Organization(name="Demo NGO", org_type="ngo")
        db.add(org)
        db.commit()
        db.refresh(org)

        # 2) User
        user = User(
            email="admin@demo.org",
            hashed_password=hash_password("admin123"),
            role="admin",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 3) Membership
        membership = Membership(
            user_id=user.id,
            organization_id=org.id,
            role="admin",
        )
        db.add(membership)
        db.commit()
        db.refresh(membership)

        # 4) Water Source (no risk_score on model)
        rainfall = 45.0
        water_level = 18.0

        source = WaterSource(
            name="Lake Victoria - Test",
            latitude=0.0,
            longitude=0.0,
            rainfall=rainfall,
            water_level=water_level,
            organization_id=org.id,
        )
        db.add(source)
        db.commit()
        db.refresh(source)

        # 5) Initial risk history row (tracks risk_score)
        initial_risk = calculate_risk(rainfall, water_level)
        db.add(
            RiskHistory(
                water_source_id=source.id,
                organization_id=org.id,
                risk_score=initial_risk,
            )
        )
        db.commit()

        print("Database seeded successfully")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
