using Microsoft.EntityFrameworkCore;

namespace WeatherForecast.DatabaseApi.Extensions;

public static class MigrationExtensions
{
    public static IHost MigrateDatabase<T>(this IHost host) where T : DbContext
    {
        using (var scope = host.Services.CreateScope())
        {
            var services = scope.ServiceProvider;
            try
            {
                var db = services.GetRequiredService<T>();
                db.Database.Migrate();
            }
            catch (Exception ex)
            {
                var logger = services.GetRequiredService<ILogger<Program>>();
                logger.LogError(ex, "Đã xảy ra lỗi khi migrate database.");
            }
        }

        return host;
    }
}