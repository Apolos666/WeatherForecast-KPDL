namespace WeatherForecast.DatabaseApi.Features.Prediction.Dtos;

public class WeatherDataDto
{
    public string Time { get; set; }
    public double TempC { get; set; }
    public int Humidity { get; set; }
    public double PressureMb { get; set; }
    public double WindKph { get; set; }
    public int Cloud { get; set; }
}

public class PredictionRequestDto
{
    public List<WeatherDataDto> weather_data { get; set; }
}

public class PredictionResponseDto
{
    public double predicted_temperature { get; set; }
    public double predicted_humidity { get; set; }
    public double predicted_cloud { get; set; }
}