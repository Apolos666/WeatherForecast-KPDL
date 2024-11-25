namespace WeatherForecast.DatabaseApi.Entities;

public class SeasonalAnalysis
{
    public int Id { get; set; }
    public DateTime Date { get; set; }
    public string YearMonth { get; set; }
    public double AvgTemp { get; set; }
    public double AvgHumidity { get; set; }
    public double TotalPrecip { get; set; }
    public double AvgWind { get; set; }
    public double AvgPressure { get; set; }
    public double MaxTemp { get; set; }
    public double MinTemp { get; set; }
    public int RainyHours { get; set; }
}
