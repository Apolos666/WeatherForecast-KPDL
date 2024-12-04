from pydantic import BaseModel, Field
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


# class SpiderChartData(BaseModel):
#     Year: int
#     Season: str
#     NumberOfDays: int

class SeasonQuantityData(BaseModel):
    year: int
    spring_quantity: int
    summer_quantity: int
    autumn_quantity: int
    winter_quantity: int    


class Centroid(BaseModel):
    SpringCentroid: float
    SummerCentroid: float
    AutumnCentroid: float
    WinterCentroid: float


class CentroidDto(BaseModel):
    id: int
    springCentroid: float
    summerCentroid: float
    autumnCentroid: float
    winterCentroid: float


class PredictionData(BaseModel):
    predicted_temperature: float
    predicted_humidity: float
    predicted_pressure: float
    predicted_wind: float
    predicted_cloud: float


class SeasonProbability(BaseModel):
    Spring: float
    Summer: float
    Autumn: float
    Winter: float

    def dict(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        for key in d:
            d[key] = round(d[key], 6)
        return d

class ClusteringResultData(BaseModel):
    centroids: Centroid
    quantity: List[SeasonQuantityData]