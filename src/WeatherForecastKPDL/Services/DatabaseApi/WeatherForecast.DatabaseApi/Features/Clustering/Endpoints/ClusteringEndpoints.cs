using System.Text;
using System.Text.Json;
using Carter;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Features.Clustering.Dtos;
using WeatherForecast.DatabaseApi.Features.Prediction.Dtos;
using WeatherForecast.DatabaseApi.Models;

namespace WeatherForecast.DatabaseApi.Features.Clustering.Endpoints;

public class ClusteringEndpoints : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapPost("/api/clustering/spiderchart", async (SpiderChartDataDto request, AppDbContext db) =>
        {
            try
            {
                var existingData = await db.SpiderChartDatas
                    .FirstOrDefaultAsync(s => s.Year == request.Year && s.Season == request.Season);

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

        app.MapPost("/api/clustering/centroid", async (CentroidDto request, AppDbContext db) =>
        {
            try
            {
                var centroid = new Centroid
                {
                    SpringCentroid = request.SpringCentroid,
                    SummerCentroid = request.SummerCentroid,
                    AutumnCentroid = request.AutumnCentroid,
                    WinterCentroid = request.WinterCentroid
                };

                db.Centroids.Add(centroid);

                await db.SaveChangesAsync();
                return Results.Ok();
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lưu dữ liệu Centroid",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/clustering/spiderchart", async (int? year, AppDbContext db) =>
        {
            try
            {
                var query = db.SpiderChartDatas.AsQueryable();

                if (year.HasValue) query = query.Where(s => s.Year == year.Value);

                var spiderChartData = await query.ToListAsync();
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

        app.MapGet("/api/clustering/centroid", async (AppDbContext db) =>
        {
            try
            {
                var centroids = await db.Centroids.OrderByDescending(c => c.Id).FirstOrDefaultAsync();
                
                return Results.Ok(centroids);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lấy dữ liệu Centroid",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/clustering/predict-season-probability", async (HttpClient httpClient, IConfiguration config) =>
        {
            try
            {
                var predictionServiceUrl = config["ClusteringServiceUrl"] ?? "http://127.0.0.1:8000";
                
                var response =
                    await httpClient.GetAsync($"{predictionServiceUrl}/api/clustering/get-precent-next-day-belong-to");

                response.EnsureSuccessStatusCode();

                var seasonProbability = await response.Content.ReadFromJsonAsync<SeasonProbabilityDto>();
                return Results.Ok(seasonProbability);
            }
            catch (HttpRequestException ex)
            {
                return Results.Problem(
                    title: "Lỗi khi gọi API Python",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });
    }
}