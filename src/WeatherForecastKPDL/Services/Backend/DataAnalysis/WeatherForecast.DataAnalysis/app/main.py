from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .core.config import settings
from .services.scheduler import WeatherAnalysisScheduler
from .core.logging import logger

scheduler = WeatherAnalysisScheduler()
async_scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động ứng dụng Weather Analysis Service")
    # Startup
    async_scheduler.add_job(
        scheduler.process_weather_data,
        'interval',
        minutes=settings.ANALYSIS_INTERVAL_MINUTES,
        next_run_time=datetime.now()
    )
    async_scheduler.start()
    
    yield
    
    logger.info("Tắt ứng dụng Weather Analysis Service")
    # Shutdown
    async_scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Weather Analysis Service is running"}