from pydantic import BaseModel

class SpiderChartData(BaseModel):
    year: int
    season: str
    half_year: str
    number_of_days: int