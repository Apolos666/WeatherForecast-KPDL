import json
from typing import List
from datetime import datetime, timedelta
import calendar
from .base import BaseWeatherConsumer
from ...models.analysis import HourlyWeatherData
from ...core.logging import logger
from kafka.structs import OffsetAndMetadata

class CorrelationWeatherConsumer(BaseWeatherConsumer):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers, "correlation_analysis")

    def get_data(self) -> List[HourlyWeatherData]:
        logger.info("Bắt đầu lấy dữ liệu cho phân tích tương quan")
        weather_data = []
        start_time = None
        end_time = None
        last_valid_offset = None
        
        try:
            while True:
                messages = self.consumer.poll(timeout_ms=5000, max_records=10000)
                if not messages:
                    break

                for tp, msgs in messages.items():
                    for msg in msgs:
                        try:
                            value = msg.value
                            if value['payload']['after'] is not None:
                                data = value['payload']['after']
                                time = datetime.strptime(data['Time'], '%Y-%m-%d %H:%M')
                                
                                # Xác định start_time và end_time cho lần đầu tiên
                                if start_time is None:
                                    start_time = time
                                    target_month = start_time.month
                                    target_year = start_time.year
                                    end_time = datetime(target_year, target_month,
                                                      calendar.monthrange(target_year, target_month)[1], 23, 0)
                                    logger.info(f"Bắt đầu lấy dữ liệu từ {start_time} đến {end_time}")
                                
                                if time > end_time:
                                    # Commit offset của message cuối cùng của tháng trước
                                    if last_valid_offset is not None:
                                        self.consumer.commit({
                                            tp: OffsetAndMetadata(last_valid_offset + 1, None)
                                        })
                                    return sorted(weather_data, key=lambda x: x.Time)
                                    
                                weather_data.append(self._process_message(data))
                                last_valid_offset = msg.offset
                        except Exception as e:
                            logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                            continue

            if last_valid_offset is not None:
                self.consumer.commit()
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đọc Kafka: {str(e)}", exc_info=True)
            raise
        finally:
            if start_time and end_time:
                logger.info(f"Đã lấy được {len(weather_data)} bản ghi từ {start_time} đến {end_time}")
                
        return weather_data