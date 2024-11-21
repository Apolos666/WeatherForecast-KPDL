using Microsoft.Extensions.Caching.Memory;

namespace WeatherForecast.DatabaseApi.Infrastructure.Services;

public class CacheService(IMemoryCache cache) : ICacheService
{
    private readonly IMemoryCache _cache = cache;
    private static readonly TimeSpan DefaultExpiration = TimeSpan.FromMinutes(10);

    public T GetOrSet<T>(string key, Func<T> getDataFunc, TimeSpan? expiration = null)
    {
        if (_cache.TryGetValue(key, out T cachedData))
        {
            return cachedData;
        }

        var data = getDataFunc();
        var cacheOptions = new MemoryCacheEntryOptions()
            .SetAbsoluteExpiration(expiration ?? DefaultExpiration);

        _cache.Set(key, data, cacheOptions);
        return data;
    }

    public async Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> getDataFunc, TimeSpan? expiration = null)
    {
        if (_cache.TryGetValue(key, out T cachedData))
        {
            return cachedData;
        }

        var data = await getDataFunc();
        var cacheOptions = new MemoryCacheEntryOptions()
            .SetAbsoluteExpiration(expiration ?? DefaultExpiration);

        _cache.Set(key, data, cacheOptions);
        return data;
    }

    public void Remove(string key)
    {
        _cache.Remove(key);
    }
}