using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Dtos;

public class ForecastDayDto
{
    [JsonPropertyName("date")]
    public DateTime Date { get; set; }

    [JsonPropertyName("date_epoch")]
    public long DateEpoch { get; set; }

    [JsonPropertyName("day")]
    public DayDto Day { get; set; }

    [JsonPropertyName("astro")]
    public AstroDto Astro { get; set; }

    [JsonPropertyName("hour")]
    public List<HourDto> Hour { get; set; }
}