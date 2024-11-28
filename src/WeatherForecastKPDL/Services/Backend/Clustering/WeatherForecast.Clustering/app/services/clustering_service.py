import logging
from app.services.data_processor import process_data
import asyncio
from app.services.database_api import send_spider_chart_data  

async def process_and_send_data(data):
    logging.info("Bắt đầu xử lý và gửi dữ liệu")
    year, seasonal_data = process_data(data)
    tasks = [
        send_spider_chart_data(year, row['Season'], row['HalfYear'], row['NumberOfDays'])
        for _, row in seasonal_data.iterrows()
    ]
    await asyncio.gather(*tasks)
    logging.info("Kết thúc xử lý và gửi dữ liệu")