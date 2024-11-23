import json
from typing import List
from .base import BaseWeatherConsumer
from ...models.analysis import HourlyWeatherData
from ...core.logging import logger

class DailyWeatherConsumer(BaseWeatherConsumer):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers, "daily_analysis")

    def get_data(self) -> List[HourlyWeatherData]:
        logger.info("Bắt đầu lấy dữ liệu 24h từ Kafka")
        try:
            weather_data = []
            message_count = 0
            
            while len(weather_data) < 24:
                messages = self.consumer.poll(timeout_ms=5000, max_records=1000)
                if not messages:
                    logger.debug("Không nhận được message mới")
                    continue
                
                for tp, msgs in messages.items():
                    for msg in msgs:
                        message_count += 1
                        logger.debug(f"Đã nhận message thứ {message_count}")
                        
                        try:
                            if msg.value['payload']['after'] is not None:
                                data = msg.value['payload']['after']
                                weather_record = self._process_message(data)
                                weather_data.append(weather_record)
                        except Exception as e:
                            logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đọc Kafka: {str(e)}", exc_info=True)
            raise
        finally:
            if weather_data:
                self.consumer.commit()
                logger.info(f"Đã lấy được {len(weather_data)} bản ghi từ Kafka")
            else:
                logger.warning("Không có dữ liệu nào được thu thập")
                
        return weather_data

    def _on_assign(self, consumer, partitions):
        logger.info(f"Được assign các partition: {partitions}")