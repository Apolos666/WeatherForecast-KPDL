from typing import List
from datetime import datetime
from .base import BaseWeatherConsumer
from ...models.analysis import HourlyWeatherData
from ...core.logging import logger
from kafka.structs import OffsetAndMetadata

class DailyWeatherConsumer(BaseWeatherConsumer):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers, "daily_analysis")
        self._last_processed_offset = None

    def _store_offset(self, partition, offset):
        """Store last processed offset to ensure continuity"""
        self._last_processed_offset = (partition, offset)
        
    def _get_starting_position(self):
        """Get the starting position for processing"""
        try:
            for partition in self.consumer.assignment():
                committed = self.consumer.committed(partition)
                current = self.consumer.position(partition)
                logger.info(f"Partition {partition.partition} - Committed: {committed}, Current: {current}")
                
                if committed is not None:
                    self.consumer.seek(partition, committed)
                    new_position = self.consumer.position(partition)
                    logger.info(f"Repositioned to committed offset: {new_position}")
                    return committed
                    
            return None
        except Exception as e:
            logger.error(f"Error getting starting position: {e}")
            return None

    def get_data(self) -> List[HourlyWeatherData]:
        logger.info("Bắt đầu lấy dữ liệu 24h từ Kafka")
        weather_data = []
        last_valid_offset = None
        last_valid_tp = None
        target_date = None
        
        try:
            while not self.consumer.assignment():
                self.consumer.poll(timeout_ms=1000)
                
            starting_offset = self._get_starting_position()
            if starting_offset:
                logger.info(f"Starting from offset: {starting_offset}")
            
            while True:
                messages = self.consumer.poll(timeout_ms=5000, max_records=1000)
                if not messages:
                    logger.debug("Không nhận được message mới")
                    break

                for tp, msgs in messages.items():
                    for msg in msgs:
                        try:
                            if msg.value['payload']['after'] is not None:
                                data = msg.value['payload']['after']
                                current_time = datetime.strptime(data['Time'], '%Y-%m-%d %H:%M')
                                
                                # Set target date from first message
                                if target_date is None:
                                    target_date = current_time.date()
                                    logger.info(f"Target date set to: {target_date}")
                                
                                # Stop if we hit a different date
                                if current_time.date() != target_date:
                                    logger.info(f"Reached different date: {current_time.date()}")
                                    return sorted(weather_data, key=lambda x: x.Time)
                                
                                weather_record = self._process_message(data)
                                weather_data.append(weather_record)
                                last_valid_offset = msg.offset
                                last_valid_tp = tp
                                
                        except Exception as e:
                            logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                            continue

        finally:
            if last_valid_offset is not None and last_valid_tp is not None:
                logger.info(f"Committing offset {last_valid_offset + 1}")
                self.consumer.commit({
                    last_valid_tp: OffsetAndMetadata(last_valid_offset + 1, None)
                })
            
            logger.info(f"Đã lấy được {len(weather_data)} bản ghi từ Kafka cho ngày {target_date}")
            
        return sorted(weather_data, key=lambda x: x.Time)