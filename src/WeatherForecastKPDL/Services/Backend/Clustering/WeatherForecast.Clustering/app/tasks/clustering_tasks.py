import ssl
from celery import Celery
import asyncio
from ..services.scheduler import WeatherClusteringScheduler
from ..core.config import settings
from ..core.logging import logger
from celery.signals import worker_ready, worker_shutdown

celery_app = Celery('weather_clustering',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    }
)

scheduler = WeatherClusteringScheduler(is_worker=settings.CELERY_WORKER)

@worker_shutdown.connect
def cleanup(sender, **kwargs):
    if scheduler.consumers:
        for consumer in scheduler.consumers.values():
            consumer.close()

@celery_app.task(name="app.tasks.clustering_tasks.process_spider_chart_clustering")
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

@celery_app.task(name="app.tasks.clustering_tasks.process_centroid_clustering")
def process_centroid_clustering():
    logger.info("Bắt đầu task phân tích centroid")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scheduler.process_centroid_clustering())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task phân tích centroid: {str(e)}")
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
    if settings.CENTROID_CLUSTERING_ENABLED:
        process_centroid_clustering.delay()

# Cấu hình schedule cho các task
beat_schedule = {}

if settings.SPIDER_CHART_CLUSTERING_ENABLED:
    beat_schedule['clustering_spider'] = {
        'task': 'app.tasks.clustering_tasks.process_spider_chart_clustering',
        'schedule': settings.SPIDER_CHART_SCHEDULE,
        'options': {'queue': 'clustering_tasks'}
    }
    
if settings.CENTROID_CLUSTERING_ENABLED:
    beat_schedule['clustering_centroid'] = {
        'task': 'app.tasks.clustering_tasks.process_centroid_clustering',
        'schedule': settings.CENTROID_SCHEDULE,
        'options': {'queue': 'clustering_tasks'}
    }

celery_app.conf.beat_schedule = beat_schedule 

celery_app.conf.task_routes = {'app.tasks.clustering_tasks.*': {'queue': 'clustering_tasks'}}

