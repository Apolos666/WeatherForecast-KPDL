from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
    DATABASE_API_URL: str = os.getenv("DATABASE_API_URL", "http://localhost:8084")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", "weather_analysis_group")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "weather-mysql.defaultdb.Hours")
    ANALYSIS_INTERVAL_MINUTES: int = int(os.getenv("ANALYSIS_INTERVAL_MINUTES", "5"))

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()