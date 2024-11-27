from pydantic import BaseModel
from typing import List

class WeatherData(BaseModel):
    Time: str
    TempC: float
    Humidity: int
    PressureMb: float
    WindKph: float
    Cloud: int

class PredictionRequest(BaseModel):
    weather_data: List[WeatherData]
