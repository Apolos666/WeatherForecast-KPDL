import ssl
from celery import Celery
import asyncio
from ..services.scheduler import WeatherClusteringScheduler
from ..core.config import settings
from ..core.logging import logger
from celery.signals import worker_ready

celery_app = Celery('weather_analysis',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
)

scheduler = WeatherClusteringScheduler(is_worker=settings.CELERY_WORKER)

@celery_app.task
def process_spider_chart_clustering():
    logger.info("Bắt đầu task phân tích spider chart")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scheduler.process_spider_chart_clustering())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task phân tích spider chart: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if loop is not None:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

@worker_ready.connect
def at_start(sender, **kwargs):
    logger.info("Worker đã sẵn sàng - Bắt đầu chạy các task ban đầu")
    if settings.SPIDER_CHART_CLUSTERING_ENABLED:
        process_spider_chart_clustering.delay()

# Cấu hình schedule cho các task
beat_schedule = {}

if settings.SPIDER_CHART_CLUSTERING_ENABLED:
    beat_schedule['clustering'] = {
        'task': 'app.tasks.weather_tasks.process_spider_chart_clustering',
        'schedule': settings.SPIDER_CHART_SCHEDULE
    }

celery_app.conf.beat_schedule = beat_schedule 