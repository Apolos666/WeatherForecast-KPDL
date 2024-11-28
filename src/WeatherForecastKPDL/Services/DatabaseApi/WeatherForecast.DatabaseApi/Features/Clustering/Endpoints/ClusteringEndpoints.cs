using Carter;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Features.Clustering.Dtos;
using WeatherForecast.DatabaseApi.Models;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Endpoints;

public class ClusteringEndpoints : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapPost("/api/analysis/spiderchart", async (SpiderChartDataDto request, AppDbContext db) =>
        {
            try
            {
                var existingData = await db.SpiderChartDatas
                    .FirstOrDefaultAsync(s => s.Year == request.Year && s.Season == request.Season && s.HalfYear == request.HalfYear);

                if (existingData != null)
                {
                    existingData.NumberOfDays = request.NumberOfDays;
                }
                else
                {
                    var spiderChartData = new SpiderChartData
                    {
                        Year = request.Year,
                        Season = request.Season,
                        HalfYear = request.HalfYear,
                        NumberOfDays = request.NumberOfDays
                    };

                    db.SpiderChartDatas.Add(spiderChartData);
                }

                await db.SaveChangesAsync();
                return Results.Ok();
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lưu dữ liệu Spider Chart",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/analysis/spiderchart", async (AppDbContext db) =>
        {
            try
            {
                var spiderChartData = await db.SpiderChartDatas
                    .OrderBy(s => s.Year)
                    .ThenBy(s => s.Season)
                    .ThenBy(s => s.HalfYear)
                    .ToListAsync();
                return Results.Ok(spiderChartData);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lấy dữ liệu Spider Chart",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });
    }
}