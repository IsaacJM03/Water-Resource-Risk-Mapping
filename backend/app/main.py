from fastapi import FastAPI

from .api import water_sources
from .utils.logger import get_logger
from app.services.scheduler import start_scheduler


app = FastAPI(title="Water Resource Risk Mapping")
logger = get_logger()

# Register routers
app.include_router(water_sources.router, prefix="/water-sources", tags=["water-sources"])


@app.get("/health")
def health_check() -> dict:
    """Lightweight health endpoint."""
    logger.debug("Health check invoked")
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    start_scheduler()