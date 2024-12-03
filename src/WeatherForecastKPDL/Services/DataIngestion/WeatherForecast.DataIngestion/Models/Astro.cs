using System.Text.Json.Serialization;

namespace WeatherForecast.DataIngestion.Models;

public class Astro
{
    [JsonPropertyName("sunrise")] public string Sunrise { get; set; }

    [JsonPropertyName("sunset")] public string Sunset { get; set; }

    [JsonPropertyName("moonrise")] public string Moonrise { get; set; }

    [JsonPropertyName("moonset")] public string Moonset { get; set; }

    [JsonPropertyName("moon_phase")] public string MoonPhase { get; set; }

    [JsonPropertyName("moon_illumination")]
    public int MoonIllumination { get; set; }
}