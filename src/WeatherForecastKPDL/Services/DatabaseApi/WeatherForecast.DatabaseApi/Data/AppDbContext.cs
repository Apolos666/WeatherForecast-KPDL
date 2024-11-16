using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Entities;
using System.Reflection;

namespace WeatherForecast.DatabaseApi.Data
{
    public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
    {
        public DbSet<Location> Locations { get; set; }
        public DbSet<Entities.WeatherForecast> WeatherForecasts { get; set; }
        public DbSet<Day> Days { get; set; }
        public DbSet<Astro> Astros { get; set; }
        public DbSet<Hour> Hours { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Tự động áp dụng tất cả các configurations trong assembly
            modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        }
    }
}