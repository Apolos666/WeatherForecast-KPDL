from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    worker_id: str = os.getenv("WORKER_ID", "default")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    DATABASE_API_URL: str = os.getenv("DATABASE_API_URL", "http://localhost:8084")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", "weather_analysis_group")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "weather-mysql.defaultdb.Hours")
    ANALYSIS_INTERVAL_MINUTES: int = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", "5"))
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    CELERY_WORKER: bool = os.getenv("CELERY_WORKER", "false").lower() == "true"

    # Schedule intervals (seconds)
    DAILY_ANALYSIS_SCHEDULE: float = 10.0  # 30 giây chạy một lần
    CORRELATION_ANALYSIS_SCHEDULE: float = 30 * 24 * 60 * 60 
    SEASONAL_ANALYSIS_SCHEDULE: float = 60  # 5 phút

    # Schedule enabled flags
    DAILY_ANALYSIS_ENABLED: bool = True
    CORRELATION_ANALYSIS_ENABLED: bool = True
    SEASONAL_ANALYSIS_ENABLED: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def celery_broker_url(self):
        if 'rediss://' in self.REDIS_URL and 'ssl_cert_reqs' not in self.REDIS_URL:
            return f"{self.REDIS_URL}?ssl_cert_reqs=CERT_NONE"
        return self.REDIS_URL

settings = Settings()