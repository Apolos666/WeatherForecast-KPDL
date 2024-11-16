using System.Text.Json.Serialization;

namespace WeatherForecast.DataIngestion.Models;

public class Condition
{
    [JsonPropertyName("text")]
    public string Text { get; set; }

    [JsonPropertyName("icon")]
    public string Icon { get; set; }

    [JsonPropertyName("code")]
    public int Code { get; set; }
}