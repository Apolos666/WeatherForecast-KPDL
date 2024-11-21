from confluent_kafka import Consumer
import json
from datetime import datetime
import pandas as pd
from typing import List
from ..models.analysis import HourlyWeatherData
from ..core.logging import logger

class WeatherKafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str):
        try:
            self.consumer = Consumer({
                'bootstrap.servers': bootstrap_servers,
                'group.id': group_id,
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': False,
            })
            logger.info("Kết nối Kafka consumer thành công")
        except Exception as e:
            logger.error(f"Lỗi khởi tạo Kafka consumer: {str(e)}")
            raise
        self.topic = 'weather-mysql.defaultdb.Hours'

    def get_24h_data(self) -> List[HourlyWeatherData]:
        logger.info("Bắt đầu lấy dữ liệu 24h từ Kafka")
        self.consumer.subscribe([self.topic])
        weather_data = []
        messages_processed = 0
        
        try:
            while len(weather_data) < 24:
                msg = self.consumer.poll(timeout=1.0)
                
                try:
                    messages_processed += 1
                    value = json.loads(msg.value().decode('utf-8'))
                    
                    if value['payload']['after'] is not None:
                        data = value['payload']['after']
                        weather_record = HourlyWeatherData(
                            Id=data['Id'],
                            WeatherForecastId=data['WeatherForecastId'],
                            TimeEpoch=data['TimeEpoch'],
                            Time=data['Time'],
                            TempC=data['TempC'],
                            Humidity=data['Humidity'],
                            PrecipMm=data['PrecipMm'],
                            WindKph=data['WindKph'],
                            PressureMb=data['PressureMb']
                        )
                        weather_data.append(weather_record)
                except Exception as e:
                    logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                    
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đọc Kafka: {str(e)}", exc_info=True)
            raise
            
        finally:
            if weather_data:
                logger.info(f"Đã lấy được {len(weather_data)} bản ghi từ Kafka")
                
                try:
                    self.consumer.commit()
                    logger.info("Đã commit offset thành công")
                except Exception as e:
                    logger.error(f"Lỗi khi commit offset: {str(e)}", exc_info=True)
            else:
                logger.warning("Không có dữ liệu nào được thu thập từ Kafka")
                
            return weather_data
        
    def get_monthly_data(self) -> List['HourlyWeatherData']:
        logger.info("Bắt đầu lấy dữ liệu cho một tháng từ Kafka")
        
        # Tạo consumer mới cho monthly data
        monthly_consumer = Consumer({
            'bootstrap.servers': self.consumer.config['bootstrap.servers'],
            'group.id': f"{self.consumer.config['group.id']}_monthly",
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        })
        
        monthly_consumer.subscribe([self.topic])
        monthly_data = []
        processed_days = set()
        
        try:
            while True:
                msg = monthly_consumer.poll(timeout=1.0)
            
                if msg is None:
                    continue
            
                try:
                    value = json.loads(msg.value().decode('utf-8'))
                    if value['payload']['after'] is not None:
                        data = value['payload']['after']
                        weather_record = HourlyWeatherData(
                            Id=data['Id'],
                            WeatherForecastId=data['WeatherForecastId'],
                            TimeEpoch=data['TimeEpoch'],
                            Time=data['Time'],
                            TempC=data['TempC'],
                            Humidity=data['Humidity'],
                            PrecipMm=data['PrecipMm'],
                            WindKph=data['WindKph'],
                            PressureMb=data['PressureMb']
                        )
                    
                        record_date = datetime.fromtimestamp(weather_record.TimeEpoch).date()
                    
                        if record_date not in processed_days and len(processed_days) < 30:
                            processed_days.add(record_date)
                            logger.info(f"Xử lý ngày: {record_date}")
                    
                        if record_date in processed_days:
                            monthly_data.append(weather_record)
                    
                        if len(processed_days) >= 30:
                            break
                except Exception as e:
                    logger.error(f"Lỗi xử lý message: {str(e)}", exc_info=True)
                    continue
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đọc Kafka: {str(e)}", exc_info=True)
            raise
        finally:
            if monthly_data:
                logger.info(f"Đã thu thập {len(monthly_data)} bản ghi từ Kafka")
                try:
                    monthly_consumer.commit()
                    logger.info("Đã commit offset thành công")
                except Exception as e:
                    logger.error(f"Lỗi khi commit offset: {str(e)}", exc_info=True)
            else:
                logger.warning("Không có dữ liệu nào được thu thập từ Kafka")
                
            # Đóng monthly consumer
            try:
                monthly_consumer.close()
                logger.info("Đã đóng Monthly Kafka consumer")
            except Exception as e:
                logger.error(f"Lỗi khi đóng Monthly Kafka consumer: {str(e)}")
        
        return monthly_data


    def __del__(self):
        try:
            self.consumer.close()
            logger.info("Đã đóng Kafka consumer")
        except Exception as e:
            logger.error(f"Lỗi khi đóng Kafka consumer: {str(e)}")
