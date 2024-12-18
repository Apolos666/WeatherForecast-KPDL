from fastapi import APIRouter, HTTPException
from app.models.prediction import PredictionRequest
from app.services.prediction_service import PredictionService
from typing import List

router = APIRouter()
prediction_service = PredictionService()

@router.post("/predict")
async def predict(request: PredictionRequest):
    try:
        prediction = prediction_service.predict(request.weather_data)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
