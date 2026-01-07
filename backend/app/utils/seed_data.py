from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.water_source import WaterSource

def seed():
    db: Session = SessionLocal()

    sources = [
        WaterSource(
            name="Kampala Borehole - Ntinda",
            latitude=0.3476,
            longitude=32.6490,
            water_level=18.5,
            rainfall=45
        ),
        WaterSource(
            name="Jinja River Intake",
            latitude=0.4244,
            longitude=33.2042,
            water_level=65,
            rainfall=120
        ),
        WaterSource(
            name="Gulu Community Well",
            latitude=2.7746,
            longitude=32.2980,
            water_level=12,
            rainfall=30
        )
    ]

    db.add_all(sources)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Data seeded successfully")