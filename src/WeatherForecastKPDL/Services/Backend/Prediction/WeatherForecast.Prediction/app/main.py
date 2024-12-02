from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.logging import logger
from .api.endpoints import prediction as prediction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động ứng dụng Weather Prediction Service")
    yield
    logger.info("Tắt ứng dụng Weather Prediction Service")

app = FastAPI(lifespan=lifespan)

app.include_router(prediction_router.router, prefix="/api/prediction", tags=["prediction"])

@app.get("/")
async def root():
    return {"message": "Weather Prediction Service is running"}