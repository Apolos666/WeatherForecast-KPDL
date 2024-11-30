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
    year: int
    quarter: int
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float
    max_temp: float
    min_temp: float
    
class CorrelationAnalysis(BaseModel):
    date: str
    temp_humidity_corr: Optional[float] = None
    temp_pressure_corr: Optional[float] = None
    temp_wind_corr: Optional[float] = None
    temp_cloud_corr: Optional[float] = None
    humidity_temp_corr: Optional[float] = None
    humidity_pressure_corr: Optional[float] = None
    humidity_wind_corr: Optional[float] = None
    humidity_cloud_corr: Optional[float] = None
    pressure_temp_corr: Optional[float] = None
    pressure_humidity_corr: Optional[float] = None
    pressure_wind_corr: Optional[float] = None
    pressure_cloud_corr: Optional[float] = None
    wind_temp_corr: Optional[float] = None
    wind_humidity_corr: Optional[float] = None
    wind_pressure_corr: Optional[float] = None
    wind_cloud_corr: Optional[float] = None
    cloud_temp_corr: Optional[float] = None
    cloud_humidity_corr: Optional[float] = None
    cloud_pressure_corr: Optional[float] = None
    cloud_wind_corr: Optional[float] = None
