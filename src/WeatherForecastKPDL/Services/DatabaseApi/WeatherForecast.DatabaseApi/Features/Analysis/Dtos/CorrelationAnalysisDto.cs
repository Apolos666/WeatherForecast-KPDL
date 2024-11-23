using System.Text.Json.Serialization;

namespace WeatherForecast.DatabaseApi.Features.Analysis.Dtos;

public class CorrelationAnalysisDto
{
    [JsonPropertyName("date")]
    public string Date { get; set; } = string.Empty;

    [JsonPropertyName("temp_humidity_corr")]
    public double TempHumidityCorr { get; set; }

    [JsonPropertyName("temp_pressure_corr")]
    public double TempPressureCorr { get; set; }

    [JsonPropertyName("temp_wind_corr")]
    public double TempWindCorr { get; set; }

    [JsonPropertyName("humidity_pressure_corr")]
    public double HumidityPressureCorr { get; set; }

    [JsonPropertyName("humidity_wind_corr")]
    public double HumidityWindCorr { get; set; }

    [JsonPropertyName("pressure_wind_corr")]
    public double PressureWindCorr { get; set; }

    [JsonPropertyName("rain_humidity_corr")]
    public double RainHumidityCorr { get; set; }

    [JsonPropertyName("feels_temp_corr")]
    public double FeelingTempCorr { get; set; }

    [JsonPropertyName("windchill_temp_corr")]
    public double WindchillTempCorr { get; set; }

    [JsonPropertyName("heatindex_temp_corr")]
    public double HeatindexTempCorr { get; set; }

    [JsonPropertyName("cloud_humidity_corr")]
    public double CloudHumidityCorr { get; set; }

    [JsonPropertyName("cloud_wind_corr")]
    public double CloudWindCorr { get; set; }
}