using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Dtos;

public class SeasonProbabilityDto
{
    public float Spring { get; set; }

    public float Summer { get; set; }

    public float Autumn { get; set; }

    public float Winter { get; set; }
}