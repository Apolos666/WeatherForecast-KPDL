using Newtonsoft.Json;
using WeatherForecast.BuildingBlock.Models;
using System.Text;

public class WeatherForecastService : BackgroundService
{
    private readonly ILogger<WeatherForecastService> _logger;
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _configuration;
    private readonly string _apiUrl;
    private readonly TimeSpan _updateInterval;
    private readonly string _databaseApiUrl;

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
        _updateInterval = TimeSpan.FromMinutes(updateIntervalMinutes);

        _databaseApiUrl = $"{_configuration["DatabaseApi:BaseUrl"]}/api/weatherdata";
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var response = await _httpClient.GetStringAsync(_apiUrl);
                var weatherData = JsonConvert.DeserializeObject<WeatherData>(response);

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
        try
        {
            var json = JsonConvert.SerializeObject(weatherData);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await _httpClient.PostAsync(_databaseApiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                _logger.LogInformation("Dữ liệu thời tiết đã được lưu thành công vào cơ sở dữ liệu");
            }
            else
            {
                _logger.LogError("Không thể lưu dữ liệu thời tiết. Mã trạng thái: {StatusCode}", response.StatusCode);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Lỗi khi gửi dữ liệu thời tiết đến DatabaseApi");
        }
    }
}
