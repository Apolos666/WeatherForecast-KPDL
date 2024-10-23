using Microsoft.EntityFrameworkCore;
using System.Reflection;
using WeatherForecast.DatabaseApi.Entities;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<WeatherData> WeatherData { get; set; }
    public DbSet<Location> Locations { get; set; }
    public DbSet<Current> CurrentWeather { get; set; }
    public DbSet<Condition> Conditions { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}

