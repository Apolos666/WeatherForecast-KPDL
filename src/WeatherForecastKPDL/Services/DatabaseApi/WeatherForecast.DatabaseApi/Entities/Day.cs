namespace WeatherForecast.DatabaseApi.Entities;

public class Day
{
    public int Id { get; set; }
    public int WeatherForecastId { get; set; }
    public WeatherForecast WeatherForecast { get; set; }

    public double MaxtempC { get; set; }
    public double MaxtempF { get; set; }
    public double MintempC { get; set; }
    public double MintempF { get; set; }
    public double AvgtempC { get; set; }
    public double AvgtempF { get; set; }
    public double MaxwindMph { get; set; }
    public double MaxwindKph { get; set; }
    public double TotalprecipMm { get; set; }
    public double TotalprecipIn { get; set; }
    public double TotalsnowCm { get; set; }
    public double AvgvisKm { get; set; }
    public double AvgvisMiles { get; set; }
    public int Avghumidity { get; set; }
    public int DailyWillItRain { get; set; }
    public int DailyChanceOfRain { get; set; }
    public int DailyWillItSnow { get; set; }
    public int DailyChanceOfSnow { get; set; }
    public string ConditionText { get; set; }
    public string ConditionIcon { get; set; }
    public int ConditionCode { get; set; }
    public double Uv { get; set; }
}