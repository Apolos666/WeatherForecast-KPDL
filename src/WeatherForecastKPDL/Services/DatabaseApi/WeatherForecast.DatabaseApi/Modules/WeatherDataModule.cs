using Carter;
using Mapster;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;
using Serilog;

namespace WeatherForecast.DatabaseApi.Modules
{
    public class WeatherDataModule : ICarterModule
    {
        public void AddRoutes(IEndpointRouteBuilder app)
        {
            app.MapPost("/api/weatherdata", async (WeatherDataDto weatherDataDto, AppDbContext dbContext) =>
            {
                var weatherData = weatherDataDto.Adapt<WeatherData>();
                weatherData.CreatedAt = DateTime.UtcNow;

                dbContext.WeatherData.Add(weatherData);
                await dbContext.SaveChangesAsync();

                // Ghi log khi thêm dữ liệu
                Log.Information("Weather data added at {Time}, ID: {Id}", weatherData.CreatedAt, weatherData.Id);

                return Results.Created($"/api/weatherdata/{weatherData.Id}", weatherData);
            });
        }
    }
}
