using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecastKPDL.Services.DatabaseApi.Data.Configurations;

public class LocationConfiguration : IEntityTypeConfiguration<Location>
{
    public void Configure(EntityTypeBuilder<Location> builder)
    {
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Name).IsRequired().HasMaxLength(100);
        builder.Property(x => x.Region).HasMaxLength(100);
        builder.Property(x => x.Country).HasMaxLength(100);
        builder.Property(x => x.TzId).HasMaxLength(50);
        builder.Property(x => x.Localtime).HasMaxLength(50);

        builder.HasIndex(x => x.Name);
    }
}