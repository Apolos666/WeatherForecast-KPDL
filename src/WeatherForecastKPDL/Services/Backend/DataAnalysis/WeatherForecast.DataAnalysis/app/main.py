from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .core.config import settings
from .services.scheduler import WeatherAnalysisScheduler
from .core.logging import logger

weather_scheduler = WeatherAnalysisScheduler()
seasonal_scheduler = WeatherAnalysisScheduler()
async_scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Khởi động ứng dụng Weather Analysis Service")
    # Startup
    async_scheduler.add_job(
        weather_scheduler.process_weather_data,
        'interval',
        minutes=settings.ANALYSIS_INTERVAL_MINUTES,
        next_run_time=datetime.now()
    )
    logger.info("Đã thêm job process_weather_data")
    
    async_scheduler.add_job(
        seasonal_scheduler.process_seasonal_data,
        'interval',
        minutes=settings.ANALYSIS_INTERVAL_MINUTES,
        next_run_time=datetime.now()
    )
    logger.info("Đã thêm job process_seasonal_data")
    
    async_scheduler.start()
    logger.info("Đã khởi động scheduler thành công")
    
    yield
    
    logger.info("Tắt ứng dụng Weather Analysis Service")
    # Shutdown
    async_scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Weather Analysis Service is running"}