from asyncio import gather
from .consumers import prediction_consumer
from .prediction_service import PredictionService
from ..core.config import settings
from ..core.logging import logger
from typing import Optional

class WeatherPredictionScheduler:
    _instance: Optional['WeatherPredictionScheduler'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, is_worker: bool = False):
        if not self._initialized:
            logger.info("Khởi tạo WeatherPredictionTrainingScheduler")
            self.consumers = {}
            if is_worker:
                self._initialize_consumers()
            self.prediction_service = PredictionService()
            self._initialized = True
    
    def _initialize_consumers(self):
        """Khởi tạo consumers theo yêu cầu"""
        self.consumers = {
            'prediction': prediction_consumer.PredictionWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
        }

    async def process_prediction_training(self):
        logger.info("Bắt đầu traing dữ liệu")
        try:
            if 'prediction' not in self.consumers:
                self.consumers['prediction'] = prediction_consumer.PredictionWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            training_data = self.consumers['prediction'].get_data()
            if training_data:
                self.prediction_service.train_model(training_data)
                logger.info("Hoàn thành traing dữ liệu")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình traing dữ liệu: {str(e)}")
            raise 