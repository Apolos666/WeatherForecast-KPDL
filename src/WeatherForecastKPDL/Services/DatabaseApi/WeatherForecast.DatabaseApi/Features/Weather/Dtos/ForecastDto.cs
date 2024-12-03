using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Dtos;

public class ForecastDto
{
    [JsonPropertyName("forecastday")] public List<ForecastDayDto> ForecastDay { get; set; }
}