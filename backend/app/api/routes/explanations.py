from fastapi import APIRouter
from app.explainability.engine import explain_risk

router = APIRouter()

@router.get("/sources/{source_id}/explanation")
def get_explanation(source_id: int):
    # fetch source, risk, trend
    
    return explanation.dict()
