using Microsoft.Extensions.Caching.Memory;

namespace WeatherForecast.DatabaseApi.Infrastructure.Services;

public class MemoryCacheService(IMemoryCache cache) : ICacheService
{
    public Task<T?> GetAsync<T>(string key)
    {
        throw new NotImplementedException();
    }

    public Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> getDataFunc, TimeSpan? expiration = null)
    {
        throw new NotImplementedException();
    }

    public Task<bool> RemoveAsync(string key)
    {
        throw new NotImplementedException();
    }

    public Task<bool> SetAsync<T>(string key, T value, TimeSpan? expiration = null)
    {
        throw new NotImplementedException();
    }
}