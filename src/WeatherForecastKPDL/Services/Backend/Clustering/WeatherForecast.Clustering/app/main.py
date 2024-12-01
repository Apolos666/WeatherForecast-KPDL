from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động ứng dụng Weather Clustering Service")
    yield
    logger.info("Tắt ứng dụng Weather Clustering Service")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Weather Clustering Service is running"}