from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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

class DailyAnalysis(BaseModel):
    date: str
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float

class SeasonalAnalysis(BaseModel):
    season: str
    start_date: str
    end_date: str
    trend_data: List[float]


class MonthlyAnalysis(BaseModel):
    month_year: str
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float
    max_temp: float
    min_temp: float
    rainy_days: int
    
class CorrelationAnalysis(BaseModel):
    date: str
    correlation_matrix: dict
