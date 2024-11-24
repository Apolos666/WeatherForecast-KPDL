import os
from kafka import KafkaConsumer
from json import loads
from ...core.logging import logger
from ...models.analysis import HourlyWeatherData

class BaseWeatherConsumer:
    def __init__(self, bootstrap_servers: str, consumer_type: str):
        self.bootstrap_servers = bootstrap_servers
        worker_id = os.getenv('WORKER_ID', 'default')
        self.group_id = f"{consumer_type}_{worker_id}"
        self.topic = 'weather-mysql.defaultdb.Hours'
        self._init_consumer()

    def _init_consumer(self):
        try:
            logger.info(f"Bắt đầu khởi tạo consumer với bootstrap servers {self.bootstrap_servers}")
            
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers.split(','),
                group_id=self.group_id,
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                value_deserializer=lambda x: loads(x.decode('utf-8')),
                session_timeout_ms=10000
            )
            
            # Kiểm tra kết nối
            topics = self.consumer.topics()
            if self.topic not in topics:
                logger.error(f"Topic {self.topic} không tồn tại")
                raise ValueError(f"Topic {self.topic} không tồn tại")
                
            # Log thông tin về partitions
            partitions = self.consumer.partitions_for_topic(self.topic)
            if partitions:
                logger.info(f"Topic {self.topic} có {len(partitions)} partitions")
                
            logger.info(f"Khởi tạo và subscribe thành công consumer với group {self.group_id}")
            
        except Exception as e:
            logger.error(f"Lỗi khởi tạo consumer: {str(e)}", exc_info=True)
            raise

    def _process_message(self, data: dict) -> HourlyWeatherData:
        return HourlyWeatherData(
            Id=data['Id'],
            WeatherForecastId=data['WeatherForecastId'],
            TimeEpoch=data['TimeEpoch'],
            Time=data['Time'],
            TempC=data['TempC'],
            Humidity=data['Humidity'],
            PrecipMm=data['PrecipMm'],
            WindKph=data['WindKph'],
            PressureMb=data['PressureMb'],
            Cloud=data['Cloud'],
            FeelslikeC=data['FeelslikeC'],
            WindchillC=data['WindchillC'],
            HeatindexC=data['HeatindexC'],
            DewpointC=data['DewpointC'],
            IsDay=data['IsDay'],
            ConditionText=data['ConditionText'],
            WindDegree=data['WindDegree'],
            WindDir=data['WindDir'],
            ChanceOfRain=data['ChanceOfRain'],
            WillItRain=data['WillItRain']
        )

    def __del__(self):
        try:
            if hasattr(self, 'consumer'):
                self.consumer.close()
                logger.info(f"Đã đóng consumer group {self.group_id}")
        except Exception as e:
            logger.error(f"Lỗi khi đóng consumer: {str(e)}")