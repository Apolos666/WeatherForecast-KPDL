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
            self.consumers = None
            self.clustering_service = WeatherClusteringService()
            self.database_api = DatabaseApiService()
            self._initialized = True
            if is_worker:
                self._initialize_consumers()

    def _initialize_consumers(self):
        """Khởi tạo consumers theo yêu cầu"""
        if self.consumers is None:
            self.consumers = {
                'clustering': SpiderChartWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
            }

    async def process_clustering_season(self):
        logger.info("Bắt đầu phân tích dữ liệu phân cụm")
        try:
            if not self.consumers:
                raise RuntimeError("Consumers not initialized")
            cluster_data = self.consumers['clustering'].get_data()
            if cluster_data:
                results = await self.clustering_service.process_clustering_data(cluster_data)
                if results is not None:
                    await self.database_api.save_clustering_analysis(results)
                logger.info("Hoàn thành phân cụm dữ liệu cho năm")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình phân cụm: {str(e)}")
            raise
