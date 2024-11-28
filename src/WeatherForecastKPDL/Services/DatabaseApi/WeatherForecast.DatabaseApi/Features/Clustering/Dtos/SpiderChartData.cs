using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Dtos;

public class SpiderChartDataDto
{
    [JsonPropertyName("year")]
    public int Year { get; set; }

    [JsonPropertyName("season")]
    public string Season { get; set; }

    [JsonPropertyName("half_year")]
    public string HalfYear { get; set; }

    [JsonPropertyName("number_of_days")]
    public int NumberOfDays { get; set; }
}