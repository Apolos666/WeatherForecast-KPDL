using StackExchange.Redis;
using WeatherForecast.DataIngestion;
using WeatherForecast.DataIngestion.Services;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((hostContext, services) =>
    {
        // Cấu hình Redis
        services.AddSingleton<IConnectionMultiplexer>(sp =>
        {
            var configuration = sp.GetRequiredService<IConfiguration>();
            var redisConnection = configuration.GetConnectionString("Redis");
            var options = ConfigurationOptions.Parse(redisConnection);
            options.AbortOnConnectFail = false; // Không dừng service nếu Redis không available
            return ConnectionMultiplexer.Connect(options);
        });

        // Đăng ký Redis service
        services.AddSingleton<ILastProcessedDateService, RedisLastProcessedDateService>();

        // Cấu hình HttpClient với các tối ưu
        services.AddHttpClient<WeatherForecastService>(client =>
        {
            client.Timeout = TimeSpan.FromSeconds(30);
            client.DefaultRequestHeaders.Add("Accept", "application/json");
        })
        .SetHandlerLifetime(TimeSpan.FromMinutes(5))
        .ConfigurePrimaryHttpMessageHandler(() => new SocketsHttpHandler
        {
            PooledConnectionLifetime = TimeSpan.FromMinutes(5),
            KeepAlivePingPolicy = HttpKeepAlivePingPolicy.WithActiveRequests,
            EnableMultipleHttp2Connections = true,
            MaxConnectionsPerServer = 10,
            PooledConnectionIdleTimeout = TimeSpan.FromMinutes(2)
        });

        // Đăng ký Weather Service như một Hosted Service
        services.AddHostedService<WeatherForecastService>();
    })
    .ConfigureLogging((hostContext, logging) =>
    {
        logging.ClearProviders();
        logging.AddConsole();
        logging.AddDebug();
        logging.SetMinimumLevel(LogLevel.Information);
    })
    .Build();

await host.RunAsync();
