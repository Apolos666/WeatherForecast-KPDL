namespace WeatherForecast.DatabaseApi.Entities;

public class Astro
{
    public int Id { get; set; }
    public int WeatherForecastId { get; set; }
    public WeatherForecast WeatherForecast { get; set; }

    public string Sunrise { get; set; }
    public string Sunset { get; set; }
    public string Moonrise { get; set; }
    public string Moonset { get; set; }
    public string MoonPhase { get; set; }
    public int MoonIllumination { get; set; }
}