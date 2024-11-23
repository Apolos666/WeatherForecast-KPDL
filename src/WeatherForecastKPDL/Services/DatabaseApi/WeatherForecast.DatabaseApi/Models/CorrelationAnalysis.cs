namespace WeatherForecast.DatabaseApi.Models;

public class CorrelationAnalysis
{
    public int Id { get; set; }
    public DateTime Date { get; set; }
    public double TempHumidityCorrelation { get; set; }
    public double TempPressureCorrelation { get; set; }
    public double TempWindCorrelation { get; set; }
    public double HumidityPressureCorrelation { get; set; }
    public double HumidityWindCorrelation { get; set; }
    public double PressureWindCorrelation { get; set; }
    public double RainHumidityCorrelation { get; set; }
    public double FeelsTempCorrelation { get; set; }
    public double WindchillTempCorrelation { get; set; }
    public double HeatindexTempCorrelation { get; set; }
    public double CloudHumidityCorrelation { get; set; }
    public double CloudWindCorrelation { get; set; }
}