using System;
using System.ComponentModel.DataAnnotations;

namespace WeatherForecast.DatabaseApi.Entities
{
    public class WeatherData
    {
        [Key]
        public int Id { get; set; }
        public int LocationId { get; set; }
        public Location Location { get; set; }
        public int CurrentId { get; set; }
        public Current Current { get; set; }
        public DateTime CreatedAt { get; set; }
    }
}
