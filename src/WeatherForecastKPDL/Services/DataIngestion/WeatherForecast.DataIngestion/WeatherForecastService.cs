using System.Text;
using System.Text.Json;
using WeatherForecast.DataIngestion.Models;
using WeatherForecast.DataIngestion.Services;

namespace WeatherForecast.DataIngestion;

public class WeatherForecastService : BackgroundService
{
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _configuration;
    private readonly ILogger<WeatherForecastService> _logger;
    private readonly ILastProcessedDateService _lastProcessedDateService;
    private readonly string _apiKey;
    private readonly string _apiUrl;
    private readonly string _databaseApiUrl;
    private readonly TimeSpan _updateInterval = TimeSpan.FromHours(24);
    private readonly TimeSpan _apiDelayInterval = TimeSpan.FromSeconds(15);

    public WeatherForecastService(
        HttpClient httpClient,
        IConfiguration configuration,
        ILogger<WeatherForecastService> logger,
        ILastProcessedDateService lastProcessedDateService)
    {
        _httpClient = httpClient;
        _configuration = configuration;
        _logger = logger;
        _lastProcessedDateService = lastProcessedDateService;
        _apiKey = _configuration["WeatherApi:ApiKey"];
        _apiUrl = $"https://api.weatherapi.com/v1/history.json?key={_apiKey}&q=Da%20Nang";
        _databaseApiUrl = $"{_configuration["DatabaseApi:BaseUrl"]}/api/weatherdata";
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var currentDate = await _lastProcessedDateService.GetLastProcessedDate();
                var endDate = DateTime.Now;

                _logger.LogInformation("Bắt đầu xử lý dữ liệu từ {StartDate} đến {EndDate}",
                    currentDate.ToString("yyyy-MM-dd"), endDate.ToString("yyyy-MM-dd"));

                while (currentDate <= endDate && !stoppingToken.IsCancellationRequested)
                {
                    var dateStr = currentDate.ToString("yyyy-MM-dd");
                    var url = $"{_apiUrl}&dt={dateStr}";

                    try
                    {
                        var response = await _httpClient.GetStringAsync(url, stoppingToken);
                        var weatherData = JsonSerializer.Deserialize<WeatherApiResponse>(response);

                        if (weatherData != null)
                        {
                            await ProcessWeatherData(weatherData, stoppingToken);
                            await _lastProcessedDateService.SaveLastProcessedDate(currentDate);
                            _logger.LogInformation("Đã xử lý dữ liệu cho ngày {Date}", dateStr);
                        }
                    }
                    catch (HttpRequestException ex)
                    {
                        _logger.LogError(ex, "Lỗi khi gọi Weather API cho ngày {Date}", dateStr);
                        await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
                        continue;
                    }

                    currentDate = currentDate.AddDays(1);
                    await Task.Delay(_apiDelayInterval, stoppingToken);
                }

                _logger.LogInformation("Hoàn thành chu kỳ xử lý dữ liệu. Đợi {Interval} giờ cho lần chạy tiếp theo",
                    _updateInterval.TotalHours);
                await Task.Delay(_updateInterval, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Lỗi không mong muốn trong quá trình xử lý dữ liệu");
                await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
            }
        }
    }

    private async Task ProcessWeatherData(WeatherApiResponse weatherData, CancellationToken stoppingToken)
    {
        try
        {
            using var content = new StringContent(
                JsonSerializer.Serialize(weatherData),
                Encoding.UTF8,
                "application/json");

            using var response = await _httpClient.PostAsync(_databaseApiUrl, content, stoppingToken);

            if (response.IsSuccessStatusCode)
            {
                _logger.LogInformation("Đã lưu thành công dữ liệu thời tiết cho {Location} vào database",
                    weatherData.Location.Name);
            }
            else
            {
                _logger.LogError("Lỗi khi lưu dữ liệu thời tiết. Status code: {StatusCode}, Content: {Content}",
                    response.StatusCode,
                    await response.Content.ReadAsStringAsync(stoppingToken));
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Lỗi khi gửi dữ liệu thời tiết đến DatabaseApi");
            throw;
        }
    }
}