from asyncio.log import logger
import traceback
from fastapi import APIRouter, HTTPException
from app.services.clustering_process import WeatherClusteringService
from typing import List
from app.models.clustering import SeasonProbability 

router = APIRouter()
clustering_service = WeatherClusteringService()

@router.get("/get-precent-next-day-belong-to")
async def predict_with_probability():
    try:
        data = await clustering_service.process_prediction_with_probability()
        logger.info(f"Kết quả dự đoán mùa của ngày tiếp theo: {data}")
        return data
    except Exception as e:
        logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
