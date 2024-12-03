using System.Text.Json.Serialization;

namespace WeatherForecast.DataIngestion.Models;

public class ForecastDay
{
    [JsonPropertyName("date")] public string Date { get; set; }

    [JsonPropertyName("date_epoch")] public long DateEpoch { get; set; }

    [JsonPropertyName("day")] public Day Day { get; set; }

    [JsonPropertyName("astro")] public Astro Astro { get; set; }

    [JsonPropertyName("hour")] public List<Hour> Hour { get; set; }
}