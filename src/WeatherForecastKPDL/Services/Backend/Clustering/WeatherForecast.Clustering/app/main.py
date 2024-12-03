from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.logging import logger
from .api.endpoints import clustering as clustering_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động ứng dụng Weather Clustering Service")
    yield
    logger.info("Tắt ứng dụng Weather Clustering Service")

app = FastAPI(lifespan=lifespan)

app.include_router(clustering_router.router, prefix="/api/clustering", tags=["clustering"])

@app.get("/")
async def root():
    return {"message": "Weather Clustering Service is running"}

