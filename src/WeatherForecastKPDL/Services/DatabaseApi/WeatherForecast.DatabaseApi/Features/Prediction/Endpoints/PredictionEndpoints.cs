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
                    var today = DateTime.UtcNow.Date;
                    var eightDaysAgo = today.AddDays(-8).ToString("yyyy-MM-dd HH:mm:ss");
                    var yesterday = today.AddDays(-1).ToString("yyyy-MM-dd HH:mm:ss");

                    var hourlyData = await context.Hours
                        .Where(h => h.Time.CompareTo(eightDaysAgo) >= 0 &&
                                    h.Time.CompareTo(yesterday) <= 0)
                        .ToListAsync();

                    // Group by theo ngày và tính trung bình
                    var dailyAverages = hourlyData
                        .GroupBy(h => DateTime.Parse(h.Time).Date)
                        .Select(g => new WeatherDataDto
                        {
                            Time = g.Key.ToString("yyyy-MM-dd"),
                            TempC = g.Average(h => h.TempC),
                            Humidity = (int)g.Average(h => h.Humidity),
                            PressureMb = g.Average(h => h.PressureMb),
                            WindKph = g.Average(h => h.WindKph),
                            Cloud = (int)g.Average(h => h.Cloud)
                        })
                        .OrderBy(d => d.Time)
                        .ToList();

                    if (dailyAverages.Count < 7)
                        return Results.BadRequest(
                            $"Không đủ dữ liệu để dự đoán. Cần 7 ngày dữ liệu, hiện chỉ có {dailyAverages.Count} ngày.");

                    // Lấy chính xác 7 ngày gần nhất
                    var last7Days = dailyAverages.TakeLast(7).ToList();

                    var predictionRequest = new PredictionRequestDto
                    {
                        weather_data = last7Days
                    };

                    var predictionServiceUrl = config["PredictionServiceUrl"] ?? "http://127.0.0.1:8000";
                    var json = JsonSerializer.Serialize(predictionRequest);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    var response =
                        await httpClient.PostAsync($"{predictionServiceUrl}/api/prediction/predict", content);

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
            });
    }
}