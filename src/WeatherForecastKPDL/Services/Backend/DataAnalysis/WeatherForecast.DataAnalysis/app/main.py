from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động ứng dụng Weather Analysis Service")
    yield
    logger.info("Tắt ứng dụng Weather Analysis Service")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Weather Analysis Service is running"}