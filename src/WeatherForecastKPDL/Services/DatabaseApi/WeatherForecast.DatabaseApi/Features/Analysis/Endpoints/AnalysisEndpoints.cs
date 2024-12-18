using Carter;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;
using WeatherForecast.DatabaseApi.Features.Analysis.Dtos;
using WeatherForecast.DatabaseApi.Features.Analysis.Hubs;
using WeatherForecast.DatabaseApi.Models;

namespace WeatherForecast.DatabaseApi.Features.Analysis.Endpoints;

public class AnalysisEndpoints : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapPost("/api/analysis/daily", async (DailyAnalysisDto request, AppDbContext db, IHubContext<AnalysisHub, IAnalysisClient> hubContext) =>
        {
            try
            {
                var date = DateTime.Parse(request.Date);
                var existingAnalysis = await db.DailyAnalyses
                    .FirstOrDefaultAsync(d => d.Date.Date == date.Date);

                DailyAnalysis analysis;
                if (existingAnalysis != null)
                {
                    existingAnalysis.AverageTemperature = request.AvgTemp;
                    existingAnalysis.AverageHumidity = request.AvgHumidity;
                    existingAnalysis.TotalPrecipitation = request.TotalPrecip;
                    existingAnalysis.AverageWindSpeed = request.AvgWind;
                    existingAnalysis.AveragePressure = request.AvgPressure;
                    analysis = existingAnalysis;
                }
                else
                {
                    analysis = new DailyAnalysis
                    {
                        Date = date,
                        AverageTemperature = request.AvgTemp,
                        AverageHumidity = request.AvgHumidity,
                        TotalPrecipitation = request.TotalPrecip,
                        AverageWindSpeed = request.AvgWind,
                        AveragePressure = request.AvgPressure
                    };
                    db.DailyAnalyses.Add(analysis);
                }

                await db.SaveChangesAsync();
                
                // Notify connected clients
                await hubContext.Clients.All.ReceiveDailyAnalysis(analysis);

                return Results.Ok();
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lưu dữ liệu phân tích",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapPost("/api/analysis/correlation", async (CorrelationAnalysisDto request, AppDbContext db) =>
        {
            try
            {
                var date = request.Date;

                var existingAnalysis = await db.CorrelationAnalyses
                    .FirstOrDefaultAsync(d => d.Time.Date == date.Date);

                if (existingAnalysis != null)
                {
                    existingAnalysis.TempCHumidityCorrelation = request.TempCHumidityCorrelation;
                    existingAnalysis.TempCPressureMbCorrelation = request.TempCPressureMbCorrelation;
                    existingAnalysis.TempCWindKphCorrelation = request.TempCWindKphCorrelation;
                    existingAnalysis.TempCCloudCorrelation = request.TempCCloudCorrelation;
                    existingAnalysis.HumidityTempCCorrelation = request.HumidityTempCCorrelation;
                    existingAnalysis.HumidityPressureMbCorrelation = request.HumidityPressureMbCorrelation;
                    existingAnalysis.HumidityWindKphCorrelation = request.HumidityWindKphCorrelation;
                    existingAnalysis.HumidityCloudCorrelation = request.HumidityCloudCorrelation;
                    existingAnalysis.PressureMbTempCCorrelation = request.PressureMbTempCCorrelation;
                    existingAnalysis.PressureMbHumidityCorrelation = request.PressureMbHumidityCorrelation;
                    existingAnalysis.PressureMbWindKphCorrelation = request.PressureMbWindKphCorrelation;
                    existingAnalysis.PressureMbCloudCorrelation = request.PressureMbCloudCorrelation;
                    existingAnalysis.WindKphTempCCorrelation = request.WindKphTempCCorrelation;
                    existingAnalysis.WindKphHumidityCorrelation = request.WindKphHumidityCorrelation;
                    existingAnalysis.WindKphPressureMbCorrelation = request.WindKphPressureMbCorrelation;
                    existingAnalysis.WindKphCloudCorrelation = request.WindKphCloudCorrelation;
                    existingAnalysis.CloudTempCCorrelation = request.CloudTempCCorrelation;
                    existingAnalysis.CloudHumidityCorrelation = request.CloudHumidityCorrelation;
                    existingAnalysis.CloudPressureMbCorrelation = request.CloudPressureMbCorrelation;
                    existingAnalysis.CloudWindKphCorrelation = request.CloudWindKphCorrelation;
                }
                else
                {
                    var analysis = new CorrelationAnalysis
                    {
                        Time = date,
                        TempCHumidityCorrelation = request.TempCHumidityCorrelation,
                        TempCPressureMbCorrelation = request.TempCPressureMbCorrelation,
                        TempCWindKphCorrelation = request.TempCWindKphCorrelation,
                        TempCCloudCorrelation = request.TempCCloudCorrelation,
                        HumidityTempCCorrelation = request.HumidityTempCCorrelation,
                        HumidityPressureMbCorrelation = request.HumidityPressureMbCorrelation,
                        HumidityWindKphCorrelation = request.HumidityWindKphCorrelation,
                        HumidityCloudCorrelation = request.HumidityCloudCorrelation,
                        PressureMbTempCCorrelation = request.PressureMbTempCCorrelation,
                        PressureMbHumidityCorrelation = request.PressureMbHumidityCorrelation,
                        PressureMbWindKphCorrelation = request.PressureMbWindKphCorrelation,
                        PressureMbCloudCorrelation = request.PressureMbCloudCorrelation,
                        WindKphTempCCorrelation = request.WindKphTempCCorrelation,
                        WindKphHumidityCorrelation = request.WindKphHumidityCorrelation,
                        WindKphPressureMbCorrelation = request.WindKphPressureMbCorrelation,
                        WindKphCloudCorrelation = request.WindKphCloudCorrelation,
                        CloudTempCCorrelation = request.CloudTempCCorrelation,
                        CloudHumidityCorrelation = request.CloudHumidityCorrelation,
                        CloudPressureMbCorrelation = request.CloudPressureMbCorrelation,
                        CloudWindKphCorrelation = request.CloudWindKphCorrelation
                    };

                    db.CorrelationAnalyses.Add(analysis);
                }

                await db.SaveChangesAsync();
                return Results.Ok();
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lưu phân tích tương quan",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });


        app.MapPost("/api/analysis/seasonal", async (SeasonalAnalysisDto request, AppDbContext db, IHubContext<AnalysisHub, IAnalysisClient> hubContext) =>
        {
            try
            {
                var existingAnalysis = await db.SeasonalAnalyses
                    .FirstOrDefaultAsync(s => s.Date == request.Date);

                SeasonalAnalysis analysis;
                if (existingAnalysis != null)
                {
                    existingAnalysis.Date = request.Date;
                    existingAnalysis.Year = request.Year;
                    existingAnalysis.Quarter = request.Quarter;
                    existingAnalysis.AvgTemp = request.AvgTemp;
                    existingAnalysis.AvgHumidity = request.AvgHumidity;
                    existingAnalysis.TotalPrecip = request.TotalPrecip;
                    existingAnalysis.AvgWind = request.AvgWind;
                    existingAnalysis.AvgPressure = request.AvgPressure;
                    existingAnalysis.MaxTemp = request.MaxTemp;
                    existingAnalysis.MinTemp = request.MinTemp;
                    analysis = existingAnalysis;
                }
                else
                {
                    analysis = new SeasonalAnalysis
                    {
                        Date = request.Date,
                        Year = request.Year,
                        Quarter = request.Quarter,
                        AvgTemp = request.AvgTemp,
                        AvgHumidity = request.AvgHumidity,
                        TotalPrecip = request.TotalPrecip,
                        AvgWind = request.AvgWind,
                        AvgPressure = request.AvgPressure,
                        MaxTemp = request.MaxTemp,
                        MinTemp = request.MinTemp
                    };
                    db.SeasonalAnalyses.Add(analysis);
                }

                await db.SaveChangesAsync();
                
                // Notify connected clients
                await hubContext.Clients.All.ReceiveSeasonalAnalysis(analysis);

                return Results.Ok();
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lưu phân tích theo mùa",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/analysis/daily", async (AppDbContext db) =>
        {
            try
            {
                var analyses = await db.DailyAnalyses
                    .OrderBy(d => d.Date)
                    .ToListAsync();
                return Results.Ok(analyses);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lấy dữ liệu phân tích hàng ngày",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/analysis/correlation", async (int year, AppDbContext db) =>
        {
            try
            {
                var analyses = await db.CorrelationAnalyses
                    .Where(a => a.Time.Year == year)
                    .ToListAsync();

                if (analyses.Count == 0)
                    return Results.NotFound($"Không tìm thấy dữ liệu phân tích tương quan cho năm {year}");

                return Results.Ok(analyses);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lấy dữ liệu phân tích tương quan",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });

        app.MapGet("/api/analysis/seasonal", async (int? year, int? quarter, AppDbContext db) =>
        {
            try
            {
                var query = db.SeasonalAnalyses.AsQueryable();

                if (year.HasValue) query = query.Where(s => s.Year == year.Value);

                if (quarter.HasValue) query = query.Where(s => s.Quarter == quarter.Value);

                var analyses = await query
                    .OrderBy(s => s.Date)
                    .ToListAsync();

                if (analyses.Count == 0) return Results.NotFound("Không tìm thấy dữ liệu phân tích theo mùa phù hợp");

                return Results.Ok(analyses);
            }
            catch (Exception ex)
            {
                return Results.Problem(
                    title: "Lỗi khi lấy dữ liệu phân tích theo mùa",
                    detail: ex.Message,
                    statusCode: 500);
            }
        });
    }
}