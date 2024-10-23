using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Configurations
{
    public class CurrentConfiguration : IEntityTypeConfiguration<Current>
    {
        public void Configure(EntityTypeBuilder<Current> builder)
        {
            builder.HasKey(c => c.Id);
            builder.Property(c => c.LastUpdated).IsRequired().HasMaxLength(50);
            builder.Property(c => c.WindDir).IsRequired().HasMaxLength(10);

            builder.HasOne(c => c.Condition)
                .WithMany()
                .HasForeignKey(c => c.ConditionId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}
