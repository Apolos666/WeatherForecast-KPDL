from fastapi import FastAPI
from app.api.endpoints import prediction

app = FastAPI()
app.include_router(prediction.router, prefix="/api/prediction", tags=["prediction"])
