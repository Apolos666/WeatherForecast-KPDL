import json
from typing import List
from datetime import datetime
from .base import BaseWeatherConsumer
from ...models.analysis import HourlyWeatherData
from ...core.logging import logger

class CorrelationWeatherConsumer(BaseWeatherConsumer):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers, "correlation_analysis")

    def get_data(self) -> List[HourlyWeatherData]:
        logger.info("Bắt đầu lấy dữ liệu cho phân tích tương quan")
        weather_data = []
        target_month = None
        target_year = None
        message_count = 0
        
        try:
            messages = self.consumer.poll(timeout_ms=5000, max_records=1000)
            if not messages:
                logger.debug("Không nhận được message mới")
                return weather_data

            for tp, msgs in messages.items():
                for msg in msgs:
                    message_count += 1
                    logger.debug(f"Đã nhận message thứ {message_count}")
                    
                    try:
                        value = msg.value
                        if value['payload']['after'] is not None:
                            data = value['payload']['after']
                            time = datetime.strptime(data['Time'], '%Y-%m-%d %H:%M')
                            
                            # Xác định tháng cần lấy dữ liệu từ message đầu tiên
                            if target_month is None:
                                target_month = time.month
                                target_year = time.year
                                logger.info(f"Bắt đầu lấy dữ liệu cho tháng {target_month}/{target_year}")
                            
                            # Chỉ lấy dữ liệu trong tháng đã xác định
                            if time.month == target_month and time.year == target_year:
                                weather_record = self._process_message(data)
                                weather_data.append(weather_record)
                            elif target_month is not None and (time.month != target_month or time.year != target_year):
                                # Dừng khi gặp dữ liệu của tháng khác
                                break
                                
                    except Exception as e:
                        logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                        continue
                        
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đọc Kafka: {str(e)}", exc_info=True)
            raise
        finally:
            if weather_data:
                self.consumer.commit()
                logger.info(f"Đã lấy được {len(weather_data)} bản ghi từ tháng {target_month}/{target_year}")
            else:
                logger.warning("Không có dữ liệu nào được thu thập")
                
        return weather_data