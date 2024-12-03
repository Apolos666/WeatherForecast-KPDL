using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecastKPDL.Data.Configurations;

public class DayConfiguration : IEntityTypeConfiguration<Day>
{
    public void Configure(EntityTypeBuilder<Day> builder)
    {
        builder.HasKey(x => x.Id);

        builder.Property(x => x.ConditionText).HasMaxLength(100);
        builder.Property(x => x.ConditionIcon).HasMaxLength(200);

        builder.HasOne(d => d.WeatherForecast)
            .WithOne(w => w.Day)
            .HasForeignKey<Day>(d => d.WeatherForecastId);
    }
}