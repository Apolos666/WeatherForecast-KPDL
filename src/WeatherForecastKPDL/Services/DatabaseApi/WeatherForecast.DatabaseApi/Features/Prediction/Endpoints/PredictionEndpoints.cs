using System.Text;
using System.Text.Json;
using Carter;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Features.Prediction.Dtos;

namespace WeatherForecast.DatabaseApi.Features.Prediction.Endpoints;

public class PredictionEndpoints : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapGet("/api/prediction/next-day",
            async (AppDbContext context, HttpClient httpClient, IConfiguration config) =>
            {
                try
                {
                    var today = DateTime.UtcNow.Date.ToString("yyyy-MM-dd HH:mm:ss");
                    var sevenDaysAgo = DateTime.UtcNow.Date.AddDays(-6).ToString("yyyy-MM-dd HH:mm:ss");

                    var hourlyData = await context.Hours
                        .Where(h => h.Time.CompareTo(sevenDaysAgo) >= 0 && h.Time.CompareTo(today) <= 0)
                        .ToListAsync();

                    var dailyAverages = hourlyData
                        .GroupBy(h => h.Time[..10])
                        .Select(g => new WeatherDataDto
                        {
                            Time = g.Key,
                            TempC = g.Average(h => h.TempC),
                            Humidity = (int)g.Average(h => h.Humidity),
                            PressureMb = g.Average(h => h.PressureMb),
                            WindKph = g.Average(h => h.WindKph),
                            Cloud = (int)g.Average(h => h.Cloud)
                        })
                        .OrderBy(d => d.Time)
                        .ToList();

                    if (dailyAverages.Count != 7)
                        return Results.BadRequest($"Cần chính xác 7 ngày dữ liệu, hiện có {dailyAverages.Count} ngày.");

                    var predictionRequest = new PredictionRequestDto
                    {
                        weather_data = dailyAverages
                    };

                    var predictionServiceUrl = config["PredictionServiceUrl"] ?? "http://127.0.0.1:8000";
                    var json = JsonSerializer.Serialize(predictionRequest);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    var response = await httpClient.PostAsync($"{predictionServiceUrl}/api/prediction/predict", content);

                    if (!response.IsSuccessStatusCode)
                    {
                        var errorContent = await response.Content.ReadAsStringAsync();
                        return Results.Problem($"Prediction service error: {errorContent}");
                    }

                    var predictionResult = await response.Content.ReadFromJsonAsync<PredictionResponseDto>();
                    return Results.Ok(predictionResult);
                }
                catch (Exception ex)
                {
                    return Results.Problem($"Internal error: {ex.Message}");
                }
            });    }
}