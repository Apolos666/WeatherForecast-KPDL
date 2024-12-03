using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecastKPDL.Services.DatabaseApi.Data.Configurations;

public class HourConfiguration : IEntityTypeConfiguration<Hour>
{
    public void Configure(EntityTypeBuilder<Hour> builder)
    {
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Time).HasMaxLength(50);
        builder.Property(x => x.WindDir).HasMaxLength(10);
        builder.Property(x => x.ConditionText).HasMaxLength(100);
        builder.Property(x => x.ConditionIcon).HasMaxLength(200);

        builder.HasOne(h => h.WeatherForecast)
            .WithMany(w => w.Hours)
            .HasForeignKey(h => h.WeatherForecastId);
    }
}