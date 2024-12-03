using Carter;
using Mapster;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;
using WeatherForecast.DatabaseApi.Features.Weather.Dtos;
using WeatherForecast.DatabaseApi.Infrastructure.Services;

namespace WeatherForecast.DatabaseApi.Features.Weather.Endpoints;

public class WeatherEndpoints : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapPost("/api/weatherdata", async (WeatherApiResponse request, AppDbContext db) =>
        {
            try
            {
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

                    if (existingForecast != null) continue; // Bỏ qua nếu đã có dữ liệu

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

        app.MapGet("/api/weather/date-range",
            async ([AsParameters] DateRangeQueryParameters parameters, AppDbContext db, ICacheService cache) =>
            {
                try
                {
                    var cacheKey = $"weather_date_range_{parameters.FromDate:yyyyMMdd}_{parameters.ToDate:yyyyMMdd}";

                    var data = await cache.GetOrSetAsync(cacheKey,
                        async () => await GetDailyWeatherData(db, parameters.FromDate, parameters.ToDate));

                    return Results.Ok(data);
                }
                catch (Exception ex)
                {
                    return Results.Problem(
                        title: "Lỗi khi truy vấn dữ liệu",
                        detail: ex.Message,
                        statusCode: 500);
                }
            });

        app.MapGet("/api/weather/weeks-ago", async ([FromQuery] int weeksAgo, AppDbContext db, ICacheService cache) =>
        {
            try
            {
                var cacheKey = $"weather_weeks_ago_{weeksAgo}";

                var data = await cache.GetOrSetAsync(cacheKey, async () =>
                {
                    var endDate = DateTime.Now.Date;
                    var startDate = endDate.AddDays(-(weeksAgo * 7));
                    return await GetDailyWeatherData(db, startDate, endDate);
                });

                return Results.Ok(data);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi truy vấn dữ liệu",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/weather/months-ago", async ([FromQuery] int monthsAgo, AppDbContext db, ICacheService cache) =>
        {
            try
            {
                var cacheKey = $"weather_months_ago_{monthsAgo}";

                var data = await cache.GetOrSetAsync(cacheKey, async () =>
                {
                    var endDate = DateTime.Now.Date;
                    var startDate = endDate.AddMonths(-monthsAgo);
                    return await GetDailyWeatherData(db, startDate, endDate);
                });

                return Results.Ok(data);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi truy vấn dữ liệu",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });
    }

    private static async Task<List<WeatherDataResponse>> GetDailyWeatherData(
        AppDbContext db,
        DateTime startDate,
        DateTime endDate)
    {
        // In ra để debug
        Console.WriteLine($"StartDate: {startDate:yyyy-MM-dd}");
        Console.WriteLine($"EndDate: {endDate:yyyy-MM-dd}");

        var query = db.Hours
            .Include(h => h.WeatherForecast)
            .Where(h => h.WeatherForecast.Date.Date >= startDate.Date &&
                        h.WeatherForecast.Date.Date <= endDate.Date);

        // In ra số lượng record trước khi group
        var count = await query.CountAsync();
        Console.WriteLine($"Số lượng records: {count}");

        var result = await query
            .GroupBy(h => h.WeatherForecast.Date.Date)
            .Select(g => new WeatherDataResponse
            {
                Date = g.Key,
                AverageTemperature = Math.Round(g.Average(h => h.TempC), 2),
                MaxTemperature = Math.Round(g.Max(h => h.TempC), 2),
                MinTemperature = Math.Round(g.Min(h => h.TempC), 2),
                AverageHumidity = Math.Round(g.Average(h => h.Humidity), 2),
                AverageWindSpeed = Math.Round(g.Average(h => h.WindKph), 2),
                MaxWindSpeed = Math.Round(g.Max(h => h.WindKph), 2),
                TotalPrecipitation = Math.Round(g.Sum(h => h.PrecipMm), 2),
                AveragePressure = Math.Round(g.Average(h => h.PressureMb), 2),
                MostCommonCondition = g.GroupBy(h => h.ConditionText)
                    .OrderByDescending(x => x.Count())
                    .First().Key,
                MostCommonWindDirection = g.GroupBy(h => h.WindDir)
                    .OrderByDescending(x => x.Count())
                    .First().Key
            })
            .ToListAsync();

        return result;
    }
}