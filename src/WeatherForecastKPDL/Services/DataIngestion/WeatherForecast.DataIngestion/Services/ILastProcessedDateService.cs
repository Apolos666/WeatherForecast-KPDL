namespace WeatherForecast.DataIngestion.Services;

public interface ILastProcessedDateService
{
    Task<DateTime> GetLastProcessedDate();
    Task SaveLastProcessedDate(DateTime date);
}