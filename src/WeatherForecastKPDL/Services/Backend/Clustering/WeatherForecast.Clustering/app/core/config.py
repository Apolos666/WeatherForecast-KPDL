import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather-mysql.defaultdb.Hours")
KAFKA_SPIDER_CHART_CONSUMER_GROUP_ID = os.getenv("KAFKA_SPIDER_CHART_CONSUMER_GROUP_ID", "spider-chart-consumer-group")
API_URL = os.getenv("API_URL", "http://localhost:8084")