import json
from typing import List
from datetime import datetime
from .base import BaseWeatherConsumer
from ...models.analysis import HourlyWeatherData
from ...core.logging import logger

class SeasonalWeatherConsumer(BaseWeatherConsumer):
    def __init__(self, bootstrap_servers: str):
        super().__init__(bootstrap_servers, "seasonal_analysis")

    def get_data(self) -> List[HourlyWeatherData]:
        pass