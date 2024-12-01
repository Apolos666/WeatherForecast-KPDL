from asyncio import gather
from .consumers.spider_chart_consumer import SpiderChartWeatherConsumer
from .clustering_process import WeatherClusteringService
from .database_api import DatabaseApiService
from ..core.config import settings
from ..core.logging import logger
from typing import Optional

class WeatherClusteringScheduler:
    _instance: Optional['WeatherClusteringScheduler'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, is_worker: bool = False):
        if not self._initialized:
            logger.info("Khởi tạo WeatherClusteringScheduler")
            self.consumers = {}
            if is_worker:
                self._initialize_consumers()
            self.analysis_service = WeatherClusteringService()
            self.database_api = DatabaseApiService()
            self._initialized = True
    
    def _initialize_consumers(self):
        """Khởi tạo consumers theo yêu cầu"""
        self.consumers = {
            'spider_chart': SpiderChartWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
            # 'seasonal': SeasonalWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
            # 'correlation': CorrelationWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
        }

    async def process_spider_chart_clustering(self):
        logger.info("Bắt đầu phân tích dữ liệu hàng ngày")
        try:
            if 'spider_chart' not in self.consumers:
                self.consumers['spider_chart'] = SpiderChartWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            spider_chart_data = self.consumers['spider_chart'].get_data()
            if spider_chart_data:
                results = self.analysis_service.process_spider_chart(spider_chart_data)
                await self.database_api.save_spider_chart_clustering(results)
                logger.info("Hoàn thành phân tích spider chart")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình phân tích spider chart: {str(e)}")
            raise