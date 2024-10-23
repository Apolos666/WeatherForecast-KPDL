using System.ComponentModel.DataAnnotations;

namespace WeatherForecast.DatabaseApi.Entities
{
    public class Condition
    {
        [Key]
        public int Id { get; set; }
        public string Text { get; set; }
        public string Icon { get; set; }
        public int Code { get; set; }
    }
}
