import json
from typing import List
from datetime import datetime
import calendar
from .base import BaseWeatherConsumer
from ...models.analysis import HourlyWeatherData
from ...core.logging import logger
from kafka.structs import OffsetAndMetadata

class SeasonalWeatherConsumer(BaseWeatherConsumer):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers, "seasonal_analysis")

    def get_data(self) -> List[HourlyWeatherData]:
        logger.info("Bắt đầu lấy dữ liệu mùa từ Kafka")
        weather_data = []
        start_time = None
        end_time = None

        try:
            while True:
                messages = self.consumer.poll(timeout_ms=5000, max_records=10000)
                if not messages:
                    logger.info("Không còn message nào nữa, dừng tiêu thụ dữ liệu")
                    break

                for tp, msgs in messages.items():
                    for msg in msgs:
                        try:
                            value = msg.value
                            if value['payload']['after'] is not None:
                                data_point = value['payload']['after']
                                time_str = data_point['Time']
                                time = datetime.fromisoformat(time_str)
                                logger.info(f"Tiêu thụ message: {time_str}")

                                # Xác định start_time và end_time cho lần đầu tiên
                                if start_time is None:
                                    start_time = time
                                    end_time = datetime(start_time.year, 12, 31, 23, 59, 59)
                                    logger.info(f"Bắt đầu lấy dữ liệu từ {start_time} đến {end_time}")

                                if time > end_time:
                                    logger.info(f"Đã chuyển sang năm mới: {time.year}, dừng tiêu thụ dữ liệu")
                                    break

                                weather_data.append(self._process_message(data_point))

                        except Exception as e:
                            logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                            continue

                if time > end_time:
                    break

        except Exception as e:
            logger.error(f"Lỗi trong quá trình đọc Kafka: {str(e)}", exc_info=True)
            raise
        finally:
            if start_time and end_time:
                logger.info(f"Đã lấy được {len(weather_data)} bản ghi từ {start_time} đến {end_time}")
                
        return weather_data