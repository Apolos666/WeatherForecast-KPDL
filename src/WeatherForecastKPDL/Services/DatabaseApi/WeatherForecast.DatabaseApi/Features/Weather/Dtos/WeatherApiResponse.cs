using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Dtos;

public class WeatherApiResponse
{
    [JsonPropertyName("location")] public LocationDto Location { get; set; }

    [JsonPropertyName("forecast")] public ForecastDto Forecast { get; set; }
}