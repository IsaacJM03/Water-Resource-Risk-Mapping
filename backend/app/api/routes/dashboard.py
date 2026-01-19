from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.water_source import WaterSource
from app.services.dashboard_builder import build_source_dashboard
from app.schemas.water_source import WaterSourceDashboard
from app.api.deps import require_roles

router = APIRouter(prefix="/dashboard")


@router.get(
    "/sources",
    response_model=list[WaterSourceDashboard],
    dependencies=[Depends(require_roles("admin", "analyst", "viewer"))]
)
def get_dashboard(db: Session = Depends(get_db)):
    sources = db.query(WaterSource).all()

    return [
        build_source_dashboard(source, db)
        for source in sources
    ]

