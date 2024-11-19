import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logging():
    # Tạo thư mục logs nếu chưa tồn tại
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Tạo tên file log với timestamp
    log_file = log_dir / f"weather_analysis_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Cấu hình logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("weather_analysis")
    logger.setLevel(logging.DEBUG)  # Cho phép log ở mức DEBUG
    
    return logger

logger = setup_logging() 