import asyncio
from typing import List
import httpx
from ..models.clustering import CentroidDto, SpiderChartData, Centroid, PredictionData
from ..core.config import settings
from ..core.logging import logger

class DatabaseApiService:
    def __init__(self):
        logger.info("Khởi tạo DatabaseApiService")
        self.base_url = settings.DATABASE_API_URL
        
    async def save_spider_chart_clustering(self, analyses: List[SpiderChartData]):
        logger.info(f"Đang lưu spider chart cho các năm {[analysis.Year for analysis in analyses]}")
        try:
            async with httpx.AsyncClient() as client:
                tasks = []
                for analysis in analyses:
                    logger.info(f"Chuẩn bị lưu spider chart cho năm {analysis.Year}")
                    logger.info(f"Dữ liệu gửi đến API: {analysis.model_dump()}")
                    task = client.post(
                        f"{self.base_url}/api/clustering/spiderchart",
                        json=analysis.model_dump()
                    )
                    tasks.append(task)
                
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    response.raise_for_status()
                    
                logger.info("Lưu spider chart data thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu spider chart: {str(e)}")
            raise

    async def save_cluster_centroid(self, centroid: Centroid):
        logger.info(f"Đang lưu centroid")
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Dữ liệu gửi đến API: {centroid.model_dump()}")
                response = await client.post(
                    f"{self.base_url}/api/clustering/centroid",
                    json=centroid.model_dump()
                )
                response.raise_for_status()
                logger.info("Lưu centroid thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu centroid: {str(e)}")
            raise

    async def get_predict_temperature_next_day(self) -> PredictionData:
        logger.info(f"Đang lấy dữ liệu nhiệt độ dự báo cho ngày hôm sau")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/prediction/next-day"
                )
                response.raise_for_status()
                data = response.json()
                logger.info(data)
                prediction_data = PredictionData.model_validate(data)
                return prediction_data
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu nhiệt độ dự báo: {str(e)}")
            raise

    async def get_centroid(self) -> CentroidDto:
        logger.info("Đang lấy dữ liệu centroid")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/clustering/centroid"
                )
                response.raise_for_status()
                data = response.json()
                logger.info(data)
                centroid_data = CentroidDto.model_validate(data)
                return centroid_data
        except Exception as e:
            logger.error(f"Lỗi khi lấy centroid: {str(e)}")
            raise


