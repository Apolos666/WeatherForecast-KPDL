
namespace WeatherForecast.DatabaseApi.Dtos;

public class WeatherDataResponse
{
    public DateTime Date { get; set; }
    public double AverageTemperature { get; set; }
    public double MaxTemperature { get; set; }
    public double MinTemperature { get; set; }
    public double AverageHumidity { get; set; }
    public double AverageWindSpeed { get; set; }
    public double MaxWindSpeed { get; set; }
    public double TotalPrecipitation { get; set; }
    public double AveragePressure { get; set; }
    public string MostCommonCondition { get; set; }
    public string MostCommonWindDirection { get; set; }
}