namespace WeatherForecast.DatabaseApi.Entities;

public class DailyAnalysis
{
    public int Id { get; set; }
    public DateTime Date { get; set; }
    public double AverageTemperature { get; set; }
    public double AverageHumidity { get; set; }
    public double TotalPrecipitation { get; set; }
    public double AverageWindSpeed { get; set; }
    public double AveragePressure { get; set; }
}