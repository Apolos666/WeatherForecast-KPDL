namespace WeatherForecast.DatabaseApi.Entities;

public class Hour
{
    public int Id { get; set; }
    public int WeatherForecastId { get; set; }
    public WeatherForecast WeatherForecast { get; set; }

    public long TimeEpoch { get; set; }
    public string Time { get; set; }
    public double TempC { get; set; }
    public double TempF { get; set; }
    public int IsDay { get; set; }
    public string ConditionText { get; set; }
    public string ConditionIcon { get; set; }
    public int ConditionCode { get; set; }
    public double WindMph { get; set; }
    public double WindKph { get; set; }
    public int WindDegree { get; set; }
    public string WindDir { get; set; }
    public double PressureMb { get; set; }
    public double PressureIn { get; set; }
    public double PrecipMm { get; set; }
    public double PrecipIn { get; set; }
    public double SnowCm { get; set; }
    public int Humidity { get; set; }
    public int Cloud { get; set; }
    public double FeelslikeC { get; set; }
    public double FeelslikeF { get; set; }
    public double WindchillC { get; set; }
    public double WindchillF { get; set; }
    public double HeatindexC { get; set; }
    public double HeatindexF { get; set; }
    public double DewpointC { get; set; }
    public double DewpointF { get; set; }
    public int WillItRain { get; set; }
    public int ChanceOfRain { get; set; }
    public int WillItSnow { get; set; }
    public int ChanceOfSnow { get; set; }
    public double VisKm { get; set; }
    public double VisMiles { get; set; }
    public double GustMph { get; set; }
    public double GustKph { get; set; }
    public double Uv { get; set; }
}