import logging
import sys

def setup_logging():
    # Format log chi tiết
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("weather_analysis")
    logger.setLevel(logging.DEBUG)
    
    return logger

logger = setup_logging() 