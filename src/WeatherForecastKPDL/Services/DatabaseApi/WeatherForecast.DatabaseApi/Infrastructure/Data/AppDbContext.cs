using System.Reflection;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Entities;
using WeatherForecast.DatabaseApi.Models;

namespace WeatherForecast.DatabaseApi.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Location> Locations { get; set; }
    public DbSet<Entities.WeatherForecast> WeatherForecasts { get; set; }
    public DbSet<Day> Days { get; set; }
    public DbSet<Astro> Astros { get; set; }
    public DbSet<Hour> Hours { get; set; }
    public DbSet<DailyAnalysis> DailyAnalyses { get; set; }
    public DbSet<CorrelationAnalysis> CorrelationAnalyses { get; set; }
    public DbSet<SeasonalAnalysis> SeasonalAnalyses { get; set; }
    public DbSet<SpiderChartData> SpiderChartDatas { get; set; }
    public DbSet<Centroid> Centroids { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}