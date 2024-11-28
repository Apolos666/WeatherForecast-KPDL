from fastapi import FastAPI
from routes import clustering_routes
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Đăng ký các route
app.include_router(clustering_routes.router, prefix="/api/clustering", tags=["clustering"])