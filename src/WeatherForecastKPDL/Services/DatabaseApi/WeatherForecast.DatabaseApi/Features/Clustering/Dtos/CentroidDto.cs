using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Dtos;

public record CentroidDto
{
    [JsonPropertyName("year")] public int Year { get; set; }

    [JsonPropertyName("springcentroid")] public double SpringCentroid { get; set; }

    [JsonPropertyName("summercentroid")] public double SummerCentroid { get; set; }

    [JsonPropertyName("autumncentroid")] public double AutumnCentroid { get; set; }

    [JsonPropertyName("wintercentroid")] public double WinterCentroid { get; set; }
}