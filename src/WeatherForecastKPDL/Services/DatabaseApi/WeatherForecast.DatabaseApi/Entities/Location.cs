using System.ComponentModel.DataAnnotations;

namespace WeatherForecast.DatabaseApi.Entities
{
    public class Location
    {
        [Key]
        public int Id { get; set; }
        public string Name { get; set; }
        public string Country { get; set; }
        public string Localtime { get; set; }
    }
}
