using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Dtos;

public class SpiderChartDataDto
{
    [JsonPropertyName("year")] 
    public int Year { get; set; }

    [JsonPropertyName("spring_quantity")] 
    public int SpringQuantity { get; set; }

    [JsonPropertyName("summer_quantity")] 
    public int SummerQuantity { get; set; }

    [JsonPropertyName("autumn_quantity")] 
    public int AutumnQuantity { get; set; }

    [JsonPropertyName("winter_quantity")] 
    public int WinterQuantity { get; set; }
}