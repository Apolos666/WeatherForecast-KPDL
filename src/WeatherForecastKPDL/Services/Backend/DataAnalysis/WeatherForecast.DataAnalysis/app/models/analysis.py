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

class DailyAnalysis(BaseModel):
    date: str
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float

class SeasonalAnalysis(BaseModel):
    date: str
    year_month: str
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float
    max_temp: float
    min_temp: float
    rainy_hours: int
    
class CorrelationAnalysis(BaseModel):
    date: str
    temp_humidity_corr: float
    temp_pressure_corr: float
    temp_wind_corr: float
    humidity_pressure_corr: float
    humidity_wind_corr: float
    pressure_wind_corr: float
    rain_humidity_corr: float
    feels_temp_corr: float
    windchill_temp_corr: float
    heatindex_temp_corr: float
    cloud_humidity_corr: float
    cloud_wind_corr: float
