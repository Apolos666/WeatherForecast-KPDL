using Newtonsoft.Json;

namespace WeatherForecast.BuildingBlock.Models;

public class Current
{
    [JsonProperty("last_updated")]
    public string LastUpdated { get; set; }

    [JsonProperty("temp_c")]
    public double TempC { get; set; }

    [JsonProperty("temp_f")]
    public double TempF { get; set; }

    [JsonProperty("is_day")]
    public int IsDay { get; set; }

    public Condition Condition { get; set; }

    [JsonProperty("wind_mph")]
    public double WindMph { get; set; }

    [JsonProperty("wind_kph")]
    public double WindKph { get; set; }

    [JsonProperty("wind_degree")]
    public int WindDegree { get; set; }

    [JsonProperty("wind_dir")]
    public string WindDir { get; set; }

    [JsonProperty("pressure_mb")]
    public double PressureMb { get; set; }

    [JsonProperty("pressure_in")]
    public double PressureIn { get; set; }

    [JsonProperty("precip_mm")]
    public double PrecipMm { get; set; }

    [JsonProperty("precip_in")]
    public double PrecipIn { get; set; }

    public int Humidity { get; set; }
    public int Cloud { get; set; }

    [JsonProperty("feelslike_c")]
    public double FeelslikeC { get; set; }

    [JsonProperty("feelslike_f")]
    public double FeelslikeF { get; set; }

    [JsonProperty("windchill_c")]
    public double WindchillC { get; set; }

    [JsonProperty("windchill_f")]
    public double WindchillF { get; set; }

    [JsonProperty("heatindex_c")]
    public double HeatindexC { get; set; }

    [JsonProperty("heatindex_f")]
    public double HeatindexF { get; set; }

    [JsonProperty("dewpoint_c")]
    public double DewpointC { get; set; }

    [JsonProperty("dewpoint_f")]
    public double DewpointF { get; set; }

    [JsonProperty("vis_km")]
    public double VisKm { get; set; }

    [JsonProperty("vis_miles")]
    public double VisMiles { get; set; }

    public double Uv { get; set; }

    [JsonProperty("gust_mph")]
    public double GustMph { get; set; }

    [JsonProperty("gust_kph")]
    public double GustKph { get; set; }
}
