import asyncio
from typing import List
import httpx
from ..models.clustering import SpiderChartData
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
                        f"{self.base_url}/api/analysis/spiderchart",
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

    # async def save_correlation_analysis(self, analysis: CorrelationAnalysis):
    #     logger.info(f"Đang lưu phân tích tương quan cho ngày {analysis.date}")
    #     try:
    #         async with httpx.AsyncClient() as client:
    #             response = await client.post(
    #                 f"{self.base_url}/api/analysis/correlation",
    #                 json=analysis.model_dump()
    #             )
    #             response.raise_for_status()
    #         logger.info("Lưu phân tích tương quan thành công")
    #     except Exception as e:
    #         logger.error(f"Lỗi khi lưu correlation analysis: {str(e)}")
    #         raise

    # async def save_seasonal_analysis(self, analyses: List[SeasonalAnalysis]):
    #     logger.info(f"Đang lưu {len(analyses)} phân tích theo quý")
    #     try:
    #         async with httpx.AsyncClient() as client:
    #             tasks = []
    #             for analysis in analyses:
    #                 logger.info(f"Chuẩn bị lưu phân tích theo mùa cho ngày {analysis.date}")
    #                 task = client.post(
    #                     f"{self.base_url}/api/analysis/seasonal",
    #                     json=analysis.model_dump()
    #                 )
    #                 tasks.append(task)
                
    #             responses = await asyncio.gather(*tasks)
    #             for response in responses:
    #                 response.raise_for_status()
                    
    #             logger.info("Lưu phân tích theo mùa thành công")
    #     except Exception as e:
    #         logger.error(f"Lỗi khi lưu seasonal analysis: {str(e)}")
    #         raise
