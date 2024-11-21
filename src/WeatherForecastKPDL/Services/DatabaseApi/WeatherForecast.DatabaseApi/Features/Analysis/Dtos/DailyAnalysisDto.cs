using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Dtos;

public class DailyAnalysisDto
{
    [JsonPropertyName("date")]
    public string Date { get; set; }

    [JsonPropertyName("avg_temp")]
    public double AvgTemp { get; set; }

    [JsonPropertyName("avg_humidity")]
    public double AvgHumidity { get; set; }

    [JsonPropertyName("total_precip")]
    public double TotalPrecip { get; set; }

    [JsonPropertyName("avg_wind")]
    public double AvgWind { get; set; }

    [JsonPropertyName("avg_pressure")]
    public double AvgPressure { get; set; }
}