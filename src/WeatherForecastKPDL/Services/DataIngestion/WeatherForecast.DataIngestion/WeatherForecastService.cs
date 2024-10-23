using Newtonsoft.Json.Linq;

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
        _updateInterval = TimeSpan.FromMinutes(updateIntervalMinutes);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var response = await _httpClient.GetStringAsync(_apiUrl);
                var jsonData = JObject.Parse(response);
                _logger.LogInformation("Dữ liệu thời tiết: {WeatherData}", jsonData.ToString());
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Lỗi khi lấy dữ liệu thời tiết");
            }

            await Task.Delay(_updateInterval, stoppingToken);
        }
    }
}
