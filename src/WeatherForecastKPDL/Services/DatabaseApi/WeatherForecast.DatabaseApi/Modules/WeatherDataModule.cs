using Carter;
using WeatherForecast.DatabaseApi.Entities;
using WeatherForecast.DatabaseApi.Dtos;
using Mapster;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;

namespace WeatherForecast.DatabaseApi.Modules
{
    public class WeatherDataModule : ICarterModule
    {
        public void AddRoutes(IEndpointRouteBuilder app)
        {
            app.MapPost("/api/weatherdata", async (WeatherApiResponse request, AppDbContext db) =>
            {
                try
                {
                    // Kiểm tra và lấy/tạo Location
                    var location = await db.Locations
                        .FirstOrDefaultAsync(l => l.Name == request.Location.Name);

                    if (location == null)
                    {
                        location = request.Location.Adapt<Location>();
                        db.Locations.Add(location);
                        await db.SaveChangesAsync();
                    }

                    // Xử lý từng forecast
                    foreach (var forecastDay in request.Forecast.ForecastDay)
                    {
                        var existingForecast = await db.WeatherForecasts
                            .FirstOrDefaultAsync(w =>
                                w.LocationId == location.Id &&
                                w.Date.Date == forecastDay.Date.Date);

                        if (existingForecast != null)
                        {
                            continue; // Bỏ qua nếu đã có dữ liệu
                        }

                        var forecast = new Entities.WeatherForecast
                        {
                            LocationId = location.Id,
                            Date = forecastDay.Date,
                            DateEpoch = forecastDay.DateEpoch,
                            Day = forecastDay.Day.Adapt<Day>(),
                            Astro = forecastDay.Astro.Adapt<Astro>(),
                            Hours = forecastDay.Hour.Select(h => h.Adapt<Hour>()).ToList()
                        };

                        db.WeatherForecasts.Add(forecast);
                    }

                    await db.SaveChangesAsync();
                    return Results.Ok();
                }
                catch (Exception ex)
                {
                    return Results.Problem(
                        title: "Lỗi khi lưu dữ liệu",
                        detail: ex.Message,
                        statusCode: 500);
                }
            });
        }
    }
}