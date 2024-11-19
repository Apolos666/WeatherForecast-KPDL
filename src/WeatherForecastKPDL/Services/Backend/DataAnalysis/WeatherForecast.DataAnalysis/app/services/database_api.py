import httpx
from ..models.analysis import DailyAnalysis
from ..core.config import settings
from ..core.logging import logger

class DatabaseApiService:
    def __init__(self):
        logger.info("Khởi tạo DatabaseApiService")
        self.base_url = settings.DATABASE_API_URL
        
    async def save_daily_analysis(self, analysis: DailyAnalysis):
        logger.info(f"Đang lưu phân tích hàng ngày cho ngày {analysis.date}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/analysis/daily",
                    json=analysis.model_dump()
                )
                response.raise_for_status()
            logger.info("Lưu phân tích hàng ngày thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu daily analysis: {str(e)}")
            raise