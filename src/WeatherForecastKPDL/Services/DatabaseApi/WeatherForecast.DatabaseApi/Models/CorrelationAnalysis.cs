namespace WeatherForecast.DatabaseApi.Models;

public class CorrelationAnalysis
{
    public int Id { get; set; }
    public DateTime Time { get; set; }
    public double TempCHumidityCorrelation { get; set; }
    public double TempCPressureMbCorrelation { get; set; }
    public double TempCWindKphCorrelation { get; set; }
    public double TempCCloudCorrelation { get; set; }
    public double HumidityTempCCorrelation { get; set; }
    public double HumidityPressureMbCorrelation { get; set; }
    public double HumidityWindKphCorrelation { get; set; }
    public double HumidityCloudCorrelation { get; set; }
    public double PressureMbTempCCorrelation { get; set; }
    public double PressureMbHumidityCorrelation { get; set; }
    public double PressureMbWindKphCorrelation { get; set; }
    public double PressureMbCloudCorrelation { get; set; }
    public double WindKphTempCCorrelation { get; set; }
    public double WindKphHumidityCorrelation { get; set; }
    public double WindKphPressureMbCorrelation { get; set; }
    public double WindKphCloudCorrelation { get; set; }
    public double CloudTempCCorrelation { get; set; }
    public double CloudHumidityCorrelation { get; set; }
    public double CloudPressureMbCorrelation { get; set; }
    public double CloudWindKphCorrelation { get; set; }
}