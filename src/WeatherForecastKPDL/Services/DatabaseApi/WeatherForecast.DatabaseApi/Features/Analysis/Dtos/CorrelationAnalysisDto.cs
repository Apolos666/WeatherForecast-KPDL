using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Analysis.Dtos;

public class CorrelationAnalysisDto
{
    [JsonPropertyName("date")]
    public DateTime Date { get; set; }

    [JsonPropertyName("temp_humidity_corr")]
    public double TempCHumidityCorrelation { get; set; }

    [JsonPropertyName("temp_pressure_corr")]
    public double TempCPressureMbCorrelation { get; set; }

    [JsonPropertyName("temp_wind_corr")]
    public double TempCWindKphCorrelation { get; set; }

    [JsonPropertyName("temp_cloud_corr")]
    public double TempCCloudCorrelation { get; set; }

    [JsonPropertyName("humidity_temp_corr")]
    public double HumidityTempCCorrelation { get; set; }

    [JsonPropertyName("humidity_pressure_corr")]
    public double HumidityPressureMbCorrelation { get; set; }

    [JsonPropertyName("humidity_wind_corr")]
    public double HumidityWindKphCorrelation { get; set; }

    [JsonPropertyName("humidity_cloud_corr")]
    public double HumidityCloudCorrelation { get; set; }

    [JsonPropertyName("pressure_temp_corr")]
    public double PressureMbTempCCorrelation { get; set; }

    [JsonPropertyName("pressure_humidity_corr")]
    public double PressureMbHumidityCorrelation { get; set; }

    [JsonPropertyName("pressure_wind_corr")]
    public double PressureMbWindKphCorrelation { get; set; }

    [JsonPropertyName("pressure_cloud_corr")]
    public double PressureMbCloudCorrelation { get; set; }

    [JsonPropertyName("wind_temp_corr")]
    public double WindKphTempCCorrelation { get; set; }

    [JsonPropertyName("wind_humidity_corr")]
    public double WindKphHumidityCorrelation { get; set; }

    [JsonPropertyName("wind_pressure_corr")]
    public double WindKphPressureMbCorrelation { get; set; }

    [JsonPropertyName("wind_cloud_corr")]
    public double WindKphCloudCorrelation { get; set; }

    [JsonPropertyName("cloud_temp_corr")]
    public double CloudTempCCorrelation { get; set; }

    [JsonPropertyName("cloud_humidity_corr")]
    public double CloudHumidityCorrelation { get; set; }

    [JsonPropertyName("cloud_pressure_corr")]
    public double CloudPressureMbCorrelation { get; set; }

    [JsonPropertyName("cloud_wind_corr")]
    public double CloudWindKphCorrelation { get; set; }
}