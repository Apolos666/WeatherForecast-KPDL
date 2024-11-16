using StackExchange.Redis;

namespace WeatherForecast.DataIngestion.Services;

public class RedisLastProcessedDateService : ILastProcessedDateService
{
    private const string KEY = "weather:last_processed_date";
    private readonly IConnectionMultiplexer _redis;
    private readonly ILogger<RedisLastProcessedDateService> _logger;
    private readonly IConfiguration _configuration;
    private readonly DateTime _configuredStartDate;

    public RedisLastProcessedDateService(
        IConnectionMultiplexer redis,
        ILogger<RedisLastProcessedDateService> logger,
        IConfiguration configuration)
    {
        _redis = redis;
        _logger = logger;
        _configuration = configuration;

        var startDateStr = _configuration["WeatherApi:StartDate"]
            ?? throw new ArgumentNullException("WeatherApi:StartDate configuration is required");

        if (!DateTime.TryParse(startDateStr, out _configuredStartDate))
        {
            throw new ArgumentException($"Invalid StartDate format in configuration: {startDateStr}");
        }
    }

    public async Task<DateTime> GetLastProcessedDate()
    {
        try
        {
            var db = _redis.GetDatabase();
            var value = await db.StringGetAsync(KEY);

            if (value.HasValue && DateTime.TryParse(value, out DateTime date))
            {
                if (date < _configuredStartDate)
                {
                    _logger.LogWarning(
                        "Stored date {StoredDate} is earlier than configured start date {ConfiguredDate}. Using configured date.",
                        date.ToString("yyyy-MM-dd"),
                        _configuredStartDate.ToString("yyyy-MM-dd"));
                    return _configuredStartDate;
                }
                return date;
            }

            _logger.LogInformation(
                "No processed date found in Redis. Starting from configured date: {ConfiguredDate}",
                _configuredStartDate.ToString("yyyy-MM-dd"));
            return _configuredStartDate;
        }
        catch (RedisConnectionException ex)
        {
            _logger.LogError(ex, "Redis connection error when getting last processed date");
            throw new InvalidOperationException("Cannot proceed without Redis connection", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error when getting last processed date");
            throw;
        }
    }

    public async Task SaveLastProcessedDate(DateTime date)
    {
        if (date < _configuredStartDate)
        {
            throw new ArgumentException(
                $"Cannot save date {date:yyyy-MM-dd} earlier than configured start date {_configuredStartDate:yyyy-MM-dd}");
        }

        try
        {
            var db = _redis.GetDatabase();
            await db.StringSetAsync(KEY, date.ToString("O"));
            _logger.LogInformation("Successfully saved last processed date: {Date}", date.ToString("yyyy-MM-dd"));
        }
        catch (RedisConnectionException ex)
        {
            _logger.LogError(ex, "Redis connection error when saving date {Date}", date.ToString("yyyy-MM-dd"));
            throw new InvalidOperationException("Cannot proceed without Redis connection", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error when saving date {Date}", date.ToString("yyyy-MM-dd"));
            throw;
        }
    }
}