from fastapi import APIRouter, HTTPException
from app.models.prediction import PredictionRequest
from app.services.prediction_service import PredictionService

router = APIRouter()
prediction_service = PredictionService()

@router.post("/train")
async def train_model():
    try:
        score = prediction_service.train_model()
        return {"message": "Model trained successfully", "score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
async def predict(request: PredictionRequest):
    try:
        prediction = prediction_service.predict(request.start_date, request.end_date)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
