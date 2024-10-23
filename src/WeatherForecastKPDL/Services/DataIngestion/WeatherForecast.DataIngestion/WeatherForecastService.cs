using Newtonsoft.Json;
using WeatherForecast.BuildingBlock.Models;

public class WeatherForecastService : BackgroundService
{
    private readonly ILogger<WeatherForecastService> _logger;
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _configuration;
    private readonly string _apiUrl;
    private readonly TimeSpan _updateInterval;

    public WeatherForecastService(ILogger<WeatherForecastService> logger, IHttpClientFactory httpClientFactory, IConfiguration configuration)
    {
        _logger = logger;
        _httpClient = httpClientFactory.CreateClient();
        _configuration = configuration;

        var baseUrl = _configuration["WeatherApi:BaseUrl"];
        var endpoint = _configuration["WeatherApi:Endpoint"];
        var apiKey = _configuration["WeatherApi:ApiKey"];
        var location = _configuration["WeatherApi:Location"];
        _apiUrl = $"{baseUrl}/{endpoint}?key={apiKey}&q={location}";

        var updateIntervalMinutes = _configuration.GetValue<int>("WeatherApi:UpdateIntervalMinutes");
        // _updateInterval = TimeSpan.FromMinutes(updateIntervalMinutes);
        _updateInterval = TimeSpan.FromSeconds(30);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var response = await _httpClient.GetStringAsync(_apiUrl);
                var weatherData = JsonConvert.DeserializeObject<WeatherData>(response);

                // Lưu trữ dữ liệu đã lọc
                // Ví dụ: bạn có thể lưu vào cơ sở dữ liệu hoặc gửi đến một dịch vụ khác
                await ProcessWeatherData(weatherData);

                _logger.LogInformation("Dữ liệu thời tiết đã được xử lý: {WeatherData}", JsonConvert.SerializeObject(weatherData));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Lỗi khi lấy hoặc xử lý dữ liệu thời tiết");
            }

            await Task.Delay(_updateInterval, stoppingToken);
        }
    }

    private async Task ProcessWeatherData(WeatherData weatherData)
    {
        // Thực hiện xử lý dữ liệu ở đây
        // Ví dụ: lưu vào cơ sở dữ liệu, gửi thông báo, v.v.
        // Đây chỉ là một phương thức giả định, bạn cần triển khai logic xử lý thực tế
        await Task.CompletedTask;
    }
}
