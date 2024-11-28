from fastapi import APIRouter
from app.services.kafka_consumer_spider_chart import consume_spider_chart_data
import asyncio

router = APIRouter()

@router.post("/start-consumer-spider-chart")
async def start_consumer_spider_chart():
    await consume_spider_chart_data()
    return {"message": "Spider Chart Consumer stopped"}