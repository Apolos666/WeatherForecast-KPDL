import asyncio
import traceback
from typing import List
import httpx
from ..models.clustering import CentroidDto, ClusteringResultData, Centroid, PredictionData
from ..core.config import settings
from ..core.logging import logger


class DatabaseApiService:
    def __init__(self):
        logger.info("Khởi tạo DatabaseApiService")
        self.base_url = settings.DATABASE_API_URL

    async def save_clustering_analysis(self, cluster_data: ClusteringResultData):
        logger.info(f"Đang lưu dữ liệu phân cụm và centroid")
        try:
            async with httpx.AsyncClient() as client:
                seasonal_quantity_list = cluster_data.quantity
                for seasonal_quantity in seasonal_quantity_list:
                    response = await client.post(
                        f"{self.base_url}/api/clustering/spiderchart",
                        json=seasonal_quantity.model_dump()
                    )
                    response.raise_for_status()
                    logger.info(f"Lưu dữ liệu phân cụm số lượng mùa cho năm {seasonal_quantity.year} thành công")

                result_response = await client.post(
                    f"{self.base_url}/api/clustering/centroid",
                    json=cluster_data.centroids.model_dump()
                )
                result_response.raise_for_status()
                logger.info(f"Lưu dữ liệu phân cụm centroids thành công") 

        except Exception as e:
            logger.error(f"Lỗi khi lưu clustering analysis: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
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
