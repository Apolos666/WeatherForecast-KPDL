using System.Reflection;
using Carter;
using HealthChecks.UI.Client;
using Mapster;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Serilog;
using Serilog.Events;
using StackExchange.Redis;
using WeatherForecast.DatabaseApi.Data;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;
using WeatherForecast.DatabaseApi.Extensions;
using WeatherForecast.DatabaseApi.Features.Analysis.Hubs;
using WeatherForecast.DatabaseApi.Infrastructure.Services;

var builder = WebApplication.CreateBuilder(args);

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
    .WriteTo.Console()
    .WriteTo.File("logs/log-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();

builder.Host.UseSerilog();
builder.Services.AddHttpClient();

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseMySql(builder.Configuration.GetConnectionString("DefaultConnection"),
        new MySqlServerVersion(new Version(8, 0, 21))));

builder.Services.AddCarter();

builder.Services.AddHealthChecks();

builder.Services.AddSingleton<IConnectionMultiplexer>(sp =>
{
    var configuration = ConfigurationOptions.Parse(
        builder.Configuration.GetConnectionString("Redis")!);
    return ConnectionMultiplexer.Connect(configuration);
});

builder.Services.AddScoped<ICacheService, RedisCacheService>();

TypeAdapterConfig.GlobalSettings.Scan(Assembly.GetExecutingAssembly());

TypeAdapterConfig<LocationDto, Location>
    .NewConfig()
    .Map(dest => dest.Id, src => 0);

TypeAdapterConfig<DayDto, Day>
    .NewConfig()
    .Map(dest => dest.Id, src => 0);

// Add this before var app = builder.Build();
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowLocalhost", policy =>
    {
        policy.WithOrigins("http://localhost:3000")
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials();
    });
});

builder.Services.AddSignalR();

var app = builder.Build();
app.UseCors("AllowLocalhost");

app.MapHub<AnalysisHub>("/hubs/analysis");
app.MapCarter();

app.MigrateDatabase<AppDbContext>();

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse,
    ResultStatusCodes =
    {
        [HealthStatus.Healthy] = StatusCodes.Status200OK,
        [HealthStatus.Degraded] = StatusCodes.Status200OK,
        [HealthStatus.Unhealthy] = StatusCodes.Status503ServiceUnavailable
    }
});

app.Run();