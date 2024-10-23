using Carter;
using Mapster;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;

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

                return Results.Created($"/api/weatherdata/{weatherData.Id}", weatherData);
            });
        }
    }
}
