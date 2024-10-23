using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Configurations
{
    public class WeatherDataConfiguration : IEntityTypeConfiguration<WeatherData>
    {
        public void Configure(EntityTypeBuilder<WeatherData> builder)
        {
            builder.HasKey(w => w.Id);
            builder.Property(w => w.CreatedAt).IsRequired();

            builder.HasOne(w => w.Location)
                .WithMany()
                .HasForeignKey(w => w.LocationId)
                .OnDelete(DeleteBehavior.Cascade);

            builder.HasOne(w => w.Current)
                .WithMany()
                .HasForeignKey(w => w.CurrentId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}
