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
        logger.info("Bắt đầu lấy dữ liệu mùa từ Kafka")
        weather_data = []
        start_time = None
        end_time = None
        last_valid_offset = None
        last_valid_tp = None

        try:
            while not self.consumer.assignment():
                self.consumer.poll(timeout_ms=1000)
                
            starting_offset = self._get_starting_position()
            if starting_offset:
                logger.info(f"Starting from offset: {starting_offset}")

            while True:
                messages = self.consumer.poll(timeout_ms=5000, max_records=10000)
                if not messages:
                    if last_valid_offset is not None and last_valid_tp is not None:
                        logger.info(f"Committing final offset {last_valid_offset + 1}")
                        self.consumer.commit({
                            last_valid_tp: OffsetAndMetadata(last_valid_offset + 1, None)
                        })
                        self._store_offset(last_valid_tp.partition, last_valid_offset + 1)
                    break

                for tp, msgs in messages.items():
                    for msg in msgs:
                        try:
                            value = msg.value
                            if value['payload']['after'] is not None:
                                data_point = value['payload']['after']
                                time = datetime.fromisoformat(data_point['Time'])
                                
                                if start_time is None:
                                    start_time = time
                                    # Get last day of current month
                                    last_day = calendar.monthrange(time.year, time.month)[1]
                                    end_time = datetime(time.year, time.month, last_day, 23, 59, 59)
                                    logger.info(f"Processing data for month {time.year}-{time.month:02d} from {start_time} to {end_time}")
                                
                                if time > end_time:
                                    if last_valid_offset is not None:
                                        next_offset = last_valid_offset + 1
                                        logger.info(f"Committing offset {next_offset} at month boundary")
                                        self.consumer.commit({
                                            last_valid_tp: OffsetAndMetadata(next_offset, None)
                                        })
                                        self._store_offset(last_valid_tp.partition, next_offset)
                                    return sorted(weather_data, key=lambda x: x.Time)

                                weather_data.append(self._process_message(data_point))
                                last_valid_offset = msg.offset
                                last_valid_tp = tp

                        except Exception as e:
                            logger.error(f"Message processing error: {e}")
                            continue

        finally:
            if self._last_processed_offset:
                partition, offset = self._last_processed_offset
                logger.info(f"Final state - Partition: {partition}, Offset: {offset}")
            
        return sorted(weather_data, key=lambda x: x.Time)