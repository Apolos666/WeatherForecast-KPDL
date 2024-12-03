using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Dtos;

public class SpiderChartDataDto
{
    [JsonPropertyName("year")] public int Year { get; set; }

    [JsonPropertyName("season")] public string Season { get; set; }

    [JsonPropertyName("numberofdays")] public int NumberOfDays { get; set; }
}