from asyncio import gather
from .consumers import DailyWeatherConsumer, SeasonalWeatherConsumer, CorrelationWeatherConsumer
from .analysis_process import WeatherAnalysisService
from .database_api import DatabaseApiService
from ..core.config import settings
from ..core.logging import logger
from typing import Optional

class WeatherAnalysisScheduler:
    _instance: Optional['WeatherAnalysisScheduler'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, is_worker: bool = False):
        if not self._initialized:
            logger.info("Khởi tạo WeatherAnalysisScheduler")
            self.consumers = {}
            if is_worker:
                self._initialize_consumers()
            self.analysis_service = WeatherAnalysisService()
            self.database_api = DatabaseApiService()
            self._initialized = True
    
    def _initialize_consumers(self):
        """Khởi tạo consumers theo yêu cầu"""
        self.consumers = {
            'daily': DailyWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
            'seasonal': SeasonalWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
            'correlation': CorrelationWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
        }

    async def process_daily_analysis(self):
        logger.info("Bắt đầu phân tích dữ liệu hàng ngày")
        try:
            if 'daily' not in self.consumers:
                self.consumers['daily'] = DailyWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            hourly_data = self.consumers['daily'].get_data()
            if hourly_data:
                result = self.analysis_service.analyze_daily_data(hourly_data)
                await self.database_api.save_daily_analysis(result)
                logger.info("Hoàn thành phân tích hàng ngày")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình phân tích hàng ngày: {str(e)}")
            raise

    async def process_seasonal_analysis(self):
        logger.info("Bắt đầu phân tích dữ liệu theo mùa")
        try:
            if 'seasonal' not in self.consumers:
                self.consumers['seasonal'] = SeasonalWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            hourly_data = self.consumers['seasonal'].get_data()
            if hourly_data:
                result = self.analysis_service.analyze_seasonal_data(hourly_data)
                await self.database_api.save_seasonal_analysis(result)
                logger.info("Hoàn thành phân tích theo mùa")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình phân tích theo mùa: {str(e)}")
            raise
        pass

    async def process_correlation_analysis(self):
        logger.info("Bắt đầu phân tích tương quan")
        try:
            if 'correlation' not in self.consumers:
                self.consumers['correlation'] = CorrelationWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            hourly_data = self.consumers['correlation'].get_data()
            if hourly_data:
                result = self.analysis_service.analyze_correlation(hourly_data)
                await self.database_api.save_correlation_analysis(result)
                logger.info("Hoàn thành phân tích tương quan")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình phân tích tương quan: {str(e)}")
            raise 