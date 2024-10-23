using System.Text.Json.Serialization;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Dtos
{
    public class WeatherDataDto
    {
        public LocationDto Location { get; set; }
        public CurrentDto Current { get; set; }
    }

    public class LocationDto
    {
        public string Name { get; set; }
        public string Country { get; set; }
        public string Localtime { get; set; }
    }

    public class CurrentDto
    {
        [JsonPropertyName("last_updated")]
        public string LastUpdated { get; set; }

        [JsonPropertyName("temp_c")]
        public double TempC { get; set; }

        [JsonPropertyName("temp_f")]
        public double TempF { get; set; }

        [JsonPropertyName("is_day")]
        public int IsDay { get; set; }

        public ConditionDto Condition { get; set; }

        [JsonPropertyName("wind_mph")]
        public double WindMph { get; set; }

        [JsonPropertyName("wind_kph")]
        public double WindKph { get; set; }

        [JsonPropertyName("wind_degree")]
        public int WindDegree { get; set; }

        [JsonPropertyName("wind_dir")]
        public string WindDir { get; set; }

        [JsonPropertyName("pressure_mb")]
        public double PressureMb { get; set; }

        [JsonPropertyName("pressure_in")]
        public double PressureIn { get; set; }

        [JsonPropertyName("precip_mm")]
        public double PrecipMm { get; set; }

        [JsonPropertyName("precip_in")]
        public double PrecipIn { get; set; }

        [JsonPropertyName("humidity")]
        public int Humidity { get; set; }

        [JsonPropertyName("cloud")]
        public int Cloud { get; set; }

        [JsonPropertyName("feelslike_c")]
        public double FeelslikeC { get; set; }

        [JsonPropertyName("feelslike_f")]
        public double FeelslikeF { get; set; }

        [JsonPropertyName("windchill_c")]
        public double WindchillC { get; set; }

        [JsonPropertyName("windchill_f")]
        public double WindchillF { get; set; }

        [JsonPropertyName("heatindex_c")]
        public double HeatindexC { get; set; }

        [JsonPropertyName("heatindex_f")]
        public double HeatindexF { get; set; }

        [JsonPropertyName("dewpoint_c")]
        public double DewpointC { get; set; }

        [JsonPropertyName("dewpoint_f")]
        public double DewpointF { get; set; }

        [JsonPropertyName("vis_km")]
        public double VisKm { get; set; }

        [JsonPropertyName("vis_miles")]
        public double VisMiles { get; set; }

        [JsonPropertyName("uv")]
        public double Uv { get; set; }

        [JsonPropertyName("gust_mph")]
        public double GustMph { get; set; }

        [JsonPropertyName("gust_kph")]
        public double GustKph { get; set; }
    }

    public class ConditionDto
    {
        public string Text { get; set; }
        public string Icon { get; set; }
        public int Code { get; set; }
    }
}
