using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Features.Analysis.Hubs
{
    public interface IAnalysisClient
    {
        Task ReceiveDailyAnalysis(DailyAnalysis dailyAnalysis);
        Task ReceiveSeasonalAnalysis(SeasonalAnalysis seasonalAnalysis);
    }
}