using System.Text.Json.Serialization;

namespace WeatherForecast.DataIngestion.Models;

public class Forecast
{
    [JsonPropertyName("forecastday")] public List<ForecastDay> ForecastDay { get; set; }
}