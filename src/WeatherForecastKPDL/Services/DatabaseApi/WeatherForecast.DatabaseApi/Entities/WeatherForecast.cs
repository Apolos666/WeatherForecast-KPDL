namespace WeatherForecast.DatabaseApi.Entities;

public class WeatherForecast
{
    public int Id { get; set; }
    public int LocationId { get; set; }
    public Location Location { get; set; }
    public DateTime Date { get; set; }
    public long DateEpoch { get; set; }

    public Day Day { get; set; }
    public Astro Astro { get; set; }
    public ICollection<Hour> Hours { get; set; }
}