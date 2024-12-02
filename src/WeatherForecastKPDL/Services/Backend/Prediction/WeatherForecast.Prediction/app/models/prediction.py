from pydantic import BaseModel
from typing import List

class HourlyWeatherData(BaseModel):
    Id: int
    WeatherForecastId: int
    TimeEpoch: int
    Time: str
    TempC: float
    Humidity: int
    PrecipMm: float
    WindKph: float
    PressureMb: float
    Cloud: int
    FeelslikeC: float
    WindchillC: float
    HeatindexC: float
    DewpointC: float
    IsDay: int
    ConditionText: str
    WindDegree: int
    WindDir: str
    ChanceOfRain: int
    WillItRain: int

class WeatherData(BaseModel):
    Time: str
    TempC: float
    Humidity: int
    PressureMb: float
    WindKph: float
    Cloud: int

class PredictionRequest(BaseModel):
    weather_data: List[WeatherData]
