namespace WeatherForecast.DatabaseApi.Infrastructure.Services;

public interface ICacheService
{
    T GetOrSet<T>(string key, Func<T> getDataFunc, TimeSpan? expiration = null);
    Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> getDataFunc, TimeSpan? expiration = null);
    void Remove(string key);
}