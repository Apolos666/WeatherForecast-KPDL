from pydantic import BaseModel

class WeatherData(BaseModel):
    Time: str
    TempC: float
    Humidity: int
    PressureMb: float
    WindKph: float
    Cloud: int

class PredictionRequest(BaseModel):
    start_date: str
    end_date: str
