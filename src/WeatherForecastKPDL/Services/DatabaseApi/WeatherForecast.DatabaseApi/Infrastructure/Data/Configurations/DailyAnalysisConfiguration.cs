using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Data.Configurations;

public class DailyAnalysisConfiguration : IEntityTypeConfiguration<DailyAnalysis>
{
    public void Configure(EntityTypeBuilder<DailyAnalysis> builder)
    {
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Date).IsRequired();
        builder.HasIndex(x => x.Date).IsUnique();
    }
}