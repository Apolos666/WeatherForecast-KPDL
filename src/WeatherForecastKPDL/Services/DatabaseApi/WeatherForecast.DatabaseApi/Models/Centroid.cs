namespace WeatherForecast.DatabaseApi.Models;

public class Centroid
{
    public int Id { get; set; }
    public double SpringCentroid { get; set; }
    public double SummerCentroid { get; set; }
    public double AutumnCentroid { get; set; }
    public double WinterCentroid { get; set; }
}