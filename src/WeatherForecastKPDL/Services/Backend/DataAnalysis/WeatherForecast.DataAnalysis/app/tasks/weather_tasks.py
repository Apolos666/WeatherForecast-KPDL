import ssl
from celery import Celery
from celery.schedules import crontab
import asyncio
from ..services.scheduler import WeatherAnalysisScheduler
from ..core.config import settings
from ..core.logging import logger
from celery.signals import worker_ready, worker_shutdown

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

scheduler = WeatherAnalysisScheduler(is_worker=settings.CELERY_WORKER)

@worker_shutdown.connect
def cleanup(sender, **kwargs):
    if scheduler.consumers:
        for consumer in scheduler.consumers.values():
            consumer.close()

@celery_app.task(name="app.tasks.weather_tasks.process_daily_analysis")
def process_daily_analysis():
    logger.info("Bắt đầu task phân tích hàng ngày")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scheduler.process_daily_analysis())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task phân tích hàng ngày: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if loop is not None:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()


@celery_app.task(name="app.tasks.weather_tasks.process_correlation_analysis")
def process_correlation_analysis():
    logger.info("Bắt đầu task phân tích tương quan")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            scheduler.process_correlation_analysis())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task phân tích tương quan: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if loop is not None:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()


@celery_app.task(name="app.tasks.weather_tasks.process_seasonal_analysis")
def process_seasonal_analysis():
    logger.info("Bắt đầu task phân tích theo mùa")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scheduler.process_seasonal_analysis())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task phân tích theo mùa: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if loop is not None:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()        

@worker_ready.connect
def at_start(sender, **kwargs):
    logger.info("Worker đã sẵn sàng - Bắt đầu chạy các task ban đầu")
    if settings.DAILY_ANALYSIS_ENABLED:
        process_daily_analysis.delay()
    if settings.CORRELATION_ANALYSIS_ENABLED:
        process_correlation_analysis.delay()
    if settings.SEASONAL_ANALYSIS_ENABLED:
        process_seasonal_analysis.delay()


# Cấu hình schedule cho các task
beat_schedule = {}

if settings.DAILY_ANALYSIS_ENABLED:
    beat_schedule['daily-analysis'] = {
        'task': 'app.tasks.weather_tasks.process_daily_analysis',
        'schedule': settings.DAILY_ANALYSIS_SCHEDULE,
        'options': {'queue': 'weather_tasks'}
    }

if settings.CORRELATION_ANALYSIS_ENABLED:
    beat_schedule['correlation-analysis'] = {
        'task': 'app.tasks.weather_tasks.process_correlation_analysis',
        'schedule': settings.CORRELATION_ANALYSIS_SCHEDULE,
        'options': {'queue': 'weather_tasks'}
    }

if settings.SEASONAL_ANALYSIS_ENABLED:
    beat_schedule['seasonal-analysis'] = {
        'task': 'app.tasks.weather_tasks.process_seasonal_analysis',
        'schedule': settings.SEASONAL_ANALYSIS_SCHEDULE,
        'options': {'queue': 'weather_tasks'}
    }

celery_app.conf.beat_schedule = beat_schedule
celery_app.conf.task_routes = {'app.tasks.weather_tasks.*': {'queue': 'weather_tasks'}}
