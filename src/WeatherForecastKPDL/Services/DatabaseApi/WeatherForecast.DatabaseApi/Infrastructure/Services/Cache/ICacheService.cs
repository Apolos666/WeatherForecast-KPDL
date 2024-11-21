namespace WeatherForecast.DatabaseApi.Infrastructure.Services;

public interface ICacheService
{
    Task<T?> GetAsync<T>(string key);
    Task<bool> SetAsync<T>(string key, T value, TimeSpan? expiration = null);
    Task<bool> RemoveAsync(string key);
    Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> getDataFunc, TimeSpan? expiration = null);
}