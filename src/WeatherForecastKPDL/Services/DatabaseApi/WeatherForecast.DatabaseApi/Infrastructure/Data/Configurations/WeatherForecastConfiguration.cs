using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecastEntities = WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecastKPDL.Services.DatabaseApi.Data.Configurations
{
    public class WeatherForecastConfiguration : IEntityTypeConfiguration<WeatherForecastEntities.WeatherForecast>
    {
        public void Configure(EntityTypeBuilder<WeatherForecastEntities.WeatherForecast> builder)
        {
            builder.HasKey(x => x.Id);

            builder.HasOne(w => w.Location)
                .WithMany(l => l.WeatherForecasts)
                .HasForeignKey(w => w.LocationId)
                .OnDelete(DeleteBehavior.Cascade);

            builder.HasIndex(x => new { x.LocationId, x.Date }).IsUnique();
        }
    }
}