using System.Text.Json.Serialization;

public class MonthlyAnalysisDto
{
    [JsonPropertyName("year_month")]
    public string YearMonth { get; set; }

    [JsonPropertyName("avg_temp")]
    public float AvgTemp { get; set; }

    [JsonPropertyName("avg_humidity")]
    public float AvgHumidity { get; set; }

    [JsonPropertyName("total_precip")]
    public float TotalPrecip { get; set; }

    [JsonPropertyName("avg_wind")]
    public float AvgWind { get; set; }

    [JsonPropertyName("avg_pressure")]
    public float AvgPressure { get; set; }

    [JsonPropertyName("max_temp")]
    public float MaxTemp { get; set; }

    [JsonPropertyName("min_temp")]
    public float MinTemp { get; set; }

    [JsonPropertyName("rainy_days")]
    public int RainyDays { get; set; }
}