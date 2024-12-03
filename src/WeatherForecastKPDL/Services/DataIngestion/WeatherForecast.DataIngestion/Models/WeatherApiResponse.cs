using System.Text.Json.Serialization;

namespace WeatherForecast.DataIngestion.Models;

public class WeatherApiResponse
{
    [JsonPropertyName("location")] public Location Location { get; set; }

    [JsonPropertyName("forecast")] public Forecast Forecast { get; set; }
}