import ssl
from celery import Celery
import asyncio
from ..services.scheduler import WeatherPredictionScheduler
from ..core.config import settings
from ..core.logging import logger
from celery.signals import worker_ready, worker_shutdown

celery_app = Celery('weather_prediction',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE
    },
)

scheduler = WeatherPredictionScheduler(is_worker=settings.CELERY_WORKER)

@worker_shutdown.connect
def cleanup(sender, **kwargs):
    if scheduler.consumers:
        for consumer in scheduler.consumers.values():
            consumer.close()

@celery_app.task(name="app.tasks.prediction_tasks.process_prediction_training")
def process_prediction_training():
    logger.info("Bắt đầu task traing dữ liệu")
    loop = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scheduler.process_prediction_training())
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Lỗi trong task traing dữ liệu: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        if loop is not None:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

@worker_ready.connect
def at_start(sender, **kwargs):
    logger.info("Worker đã sẵn sàng - Bắt đầu chạy các task ban đầu")
    if settings.PREDICTION_TRAINING_ENABLED:
        process_prediction_training.delay()
    
# Cấu hình schedule cho các task
beat_schedule = {}

if settings.PREDICTION_TRAINING_ENABLED:
    beat_schedule['prediction-training'] = {
        'task': 'app.tasks.prediction_tasks.process_prediction_training',
        'schedule': settings.PREDICTION_TRAINING_SCHEDULE,
        'options': {'queue': 'prediction_tasks'}
    }

celery_app.conf.beat_schedule = beat_schedule 
celery_app.conf.task_routes = {'app.tasks.prediction_tasks.*': {'queue': 'prediction_tasks'}}