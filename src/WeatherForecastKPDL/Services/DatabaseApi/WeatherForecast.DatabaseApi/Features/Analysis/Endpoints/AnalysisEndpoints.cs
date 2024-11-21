using Carter;
using Microsoft.EntityFrameworkCore;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Features.Analysis.Endpoints;

public class AnalysisEndpoints : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapPost("/api/analysis/daily", async (DailyAnalysisDto request, AppDbContext db) =>
        {
            try
            {
                var date = DateTime.Parse(request.Date);

                // Kiểm tra xem đã có dữ liệu cho ngày này chưa
                var existingAnalysis = await db.DailyAnalyses
                    .FirstOrDefaultAsync(d => d.Date.Date == date.Date);

                if (existingAnalysis != null)
                {
                    // Cập nhật dữ liệu hiện có
                    existingAnalysis.AverageTemperature = request.AvgTemp;
                    existingAnalysis.AverageHumidity = request.AvgHumidity;
                    existingAnalysis.TotalPrecipitation = request.TotalPrecip;
                    existingAnalysis.AverageWindSpeed = request.AvgWind;
                    existingAnalysis.AveragePressure = request.AvgPressure;
                }
                else
                {
                    // Tạo mới dữ liệu phân tích
                    var analysis = new DailyAnalysis
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
    }
}
