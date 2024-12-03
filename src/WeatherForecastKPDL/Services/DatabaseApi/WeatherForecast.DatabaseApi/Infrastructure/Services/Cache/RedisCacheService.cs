using System.Text.Json;
using StackExchange.Redis;

namespace WeatherForecast.DatabaseApi.Infrastructure.Services;

public class RedisCacheService(IConnectionMultiplexer redis) : ICacheService
{
    private static readonly TimeSpan DefaultExpiration = TimeSpan.FromMinutes(10);
    private readonly IDatabase _db = redis.GetDatabase();
    private readonly IConnectionMultiplexer _redis = redis;

    public async Task<T?> GetAsync<T>(string key)
    {
        var value = await _db.StringGetAsync(key);
        if (!value.HasValue)
            return default;

        return JsonSerializer.Deserialize<T>(value!);
    }

    public async Task<bool> SetAsync<T>(string key, T value, TimeSpan? expiration = null)
    {
        var serializedValue = JsonSerializer.Serialize(value);
        return await _db.StringSetAsync(key, serializedValue, expiration ?? DefaultExpiration);
    }

    public async Task<bool> RemoveAsync(string key)
    {
        return await _db.KeyDeleteAsync(key);
    }

    public async Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> getDataFunc, TimeSpan? expiration = null)
    {
        var value = await GetAsync<T>(key);
        if (value != null)
            return value;

        value = await getDataFunc();
        await SetAsync(key, value, expiration ?? DefaultExpiration);
        return value;
    }
}