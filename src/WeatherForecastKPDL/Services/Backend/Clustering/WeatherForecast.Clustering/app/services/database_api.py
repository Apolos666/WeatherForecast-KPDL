import logging
from app.core.config import API_URL
import httpx
import asyncio

async def send_spider_chart_data(year, season, half_year, number_of_days):
    # Chuyển đổi các giá trị thành kiểu int chuẩn
    year = int(year)
    number_of_days = int(number_of_days)

    url = f"{API_URL}/api/analysis/spiderchart"
    data = {
        "year": year,
        "season": season,
        "half_year": half_year,
        "number_of_days": number_of_days
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        if response.status_code == 200:
            logging.info(f"Đã lưu dữ liệu cho {season} - {half_year} năm {year}")
        else:
            logging.error(f"Lỗi khi lưu dữ liệu: {response.status_code} - {response.text}")