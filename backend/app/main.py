from fastapi import FastAPI, Depends

from app.models.water_source import WaterSource

from .api import water_sources
from .utils.logger import get_logger
from app.core.scheduler import start_scheduler
from fastapi import Request
from .api.water_sources import get_db
from app.api.routes import water, analytics, alerts,dashboard,realtime,explanations

app = FastAPI(title="Water Risk API", version="v1")

# Register routers
app.include_router(water.router, prefix="/sources", tags=["water"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(alerts.router, tags=["alerts"])
app.include_router(water_sources.router, prefix="/water-sources", tags=["water-sources"])
app.include_router(dashboard.router, tags=["dashboard"])
app.include_router(realtime.router)
app.include_router(explanations.router)
logger = get_logger()


@app.get("/health")
def health_check() -> dict:
    """Lightweight health endpoint."""
    logger.debug("Health check invoked")
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    start_scheduler()
    

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} {response.status_code}")
    return response

@app.get("/sources")
def list_sources(db = Depends(get_db), limit: int = 10, offset: int = 0):
    return db.query(WaterSource).limit(limit).offset(offset).all()

@app.get("/map/sources")
def map_sources(db = Depends(get_db)):
    from app.models.risk_history import RiskHistory
    from sqlalchemy import func
    
    sources = db.query(WaterSource).all()
    
    result = []
    for source in sources:
        latest_risk = db.query(RiskHistory.risk_score).filter(
            RiskHistory.water_source_id == source.id
        ).order_by(RiskHistory.recorded_at.desc()).first()
        
        risk_value = latest_risk[0] if latest_risk else 0
        
        result.append({
            "id": source.id,
            "name": source.name,
            "latitude": source.latitude,
            "longitude": source.longitude,
            "water_level": source.water_level,
            "rainfall": source.rainfall,
            "risk": risk_value
        })
    
    return result