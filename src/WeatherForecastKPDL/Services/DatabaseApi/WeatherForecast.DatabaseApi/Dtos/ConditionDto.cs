using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Dtos;

public class ConditionDto
{
    [JsonPropertyName("text")]
    public string Text { get; set; }

    [JsonPropertyName("icon")]
    public string Icon { get; set; }

    [JsonPropertyName("code")]
    public int Code { get; set; }
}