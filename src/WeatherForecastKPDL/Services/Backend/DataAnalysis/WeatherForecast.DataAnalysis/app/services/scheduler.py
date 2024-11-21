from .kafka_consumer import WeatherKafkaConsumer
from .analysis_service import WeatherAnalysisService
from .database_api import DatabaseApiService
from ..core.config import settings
from ..core.logging import logger

class WeatherAnalysisScheduler:
    def __init__(self):
        logger.info("Khởi tạo WeatherAnalysisScheduler")
        self.consumer = WeatherKafkaConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID
        )
        self.analysis_service = WeatherAnalysisService()
        self.database_api = DatabaseApiService()

    async def process_weather_data(self):
        logger.info("Bắt đầu xử lý dữ liệu thời tiết")
        try:
            hourly_data = self.consumer.get_24h_data()
            if hourly_data:
                daily_analysis = self.analysis_service.analyze_daily_data(hourly_data)
                await self.database_api.save_daily_analysis(daily_analysis)
                logger.info("Xử lý dữ liệu thời tiết thành công")
            else:
                logger.warning("Không nhận được dữ liệu từ Kafka")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý dữ liệu thời tiết: {str(e)}")
            
    async def process_seasonal_data(self):
        logger.info("Bắt đầu xử lý dữ liệu theo tháng")
        try: 
            hourly_data = self.consumer.get_monthly_data()
            if hourly_data:
                monthly_analysis = self.analysis_service.analyze_seasonal_data(hourly_data)
                await self.database_api.save_seasonal_analysis(monthly_analysis)
                logger.info("Xử lý dữ liệu theo tháng thành công")
            else:
                logger.warning("Không nhận được dữ liệu từ Kafka")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý dữ liệu theo tháng: {str(e)}")