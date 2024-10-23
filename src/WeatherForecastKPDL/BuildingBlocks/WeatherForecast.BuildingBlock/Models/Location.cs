using Newtonsoft.Json;

namespace WeatherForecast.BuildingBlock.Models;

public class Location
{
    public string Name { get; set; }
    public string Country { get; set; }
    public string Localtime { get; set; }
}
