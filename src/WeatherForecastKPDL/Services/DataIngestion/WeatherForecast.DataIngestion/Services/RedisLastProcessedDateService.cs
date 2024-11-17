using StackExchange.Redis;

namespace WeatherForecast.DataIngestion.Services;

public class RedisLastProcessedDateService : ILastProcessedDateService
{
    private const string KEY = "weather:last_processed_date";
    private readonly IConnectionMultiplexer _redis;
    private readonly ILogger<RedisLastProcessedDateService> _logger;
    private readonly DateTime _defaultStartDate;

    public RedisLastProcessedDateService(
        IConnectionMultiplexer redis,
        ILogger<RedisLastProcessedDateService> logger)
    {
        _redis = redis;
        _logger = logger;
        _defaultStartDate = DateTime.Now.AddYears(-1);
    }

    public async Task<DateTime> GetLastProcessedDate()
    {
        try
        {
            var db = _redis.GetDatabase();
            var value = await db.StringGetAsync(KEY);

            if (value.HasValue && DateTime.TryParse(value, out DateTime date))
            {
                return date;
            }

            _logger.LogInformation(
                "Không tìm thấy ngày xử lý trong Redis. Bắt đầu từ ngày mặc định: {DefaultDate}",
                _defaultStartDate.ToString("yyyy-MM-dd"));
            return _defaultStartDate;
        }
        catch (RedisConnectionException ex)
        {
            _logger.LogError(ex, "Lỗi kết nối Redis khi lấy ngày xử lý cuối cùng");
            throw new InvalidOperationException("Không thể tiếp tục khi không có kết nối Redis", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Lỗi không mong muốn khi lấy ngày xử lý cuối cùng");
            throw;
        }
    }

    public async Task SaveLastProcessedDate(DateTime date)
    {
        try
        {
            var db = _redis.GetDatabase();
            await db.StringSetAsync(KEY, date.ToString("O"));
            _logger.LogInformation("Đã lưu thành công ngày xử lý cuối cùng: {Date}", date.ToString("yyyy-MM-dd"));
        }
        catch (RedisConnectionException ex)
        {
            _logger.LogError(ex, "Lỗi kết nối Redis khi lưu ngày {Date}", date.ToString("yyyy-MM-dd"));
            throw new InvalidOperationException("Không thể tiếp tục khi không có kết nối Redis", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Lỗi không mong muốn khi lưu ngày {Date}", date.ToString("yyyy-MM-dd"));
            throw;
        }
    }
}