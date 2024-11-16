using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecastKPDL.Services.DatabaseApi.Data.Configurations
{
    public class AstroConfiguration : IEntityTypeConfiguration<Astro>
    {
        public void Configure(EntityTypeBuilder<Astro> builder)
        {
            builder.HasKey(x => x.Id);

            builder.Property(x => x.Sunrise).HasMaxLength(20);
            builder.Property(x => x.Sunset).HasMaxLength(20);
            builder.Property(x => x.Moonrise).HasMaxLength(20);
            builder.Property(x => x.Moonset).HasMaxLength(20);
            builder.Property(x => x.MoonPhase).HasMaxLength(50);

            builder.HasOne(a => a.WeatherForecast)
                .WithOne(w => w.Astro)
                .HasForeignKey<Astro>(a => a.WeatherForecastId);
        }
    }
}