using Microsoft.AspNetCore.SignalR;

namespace WeatherForecast.DatabaseApi.Features.Analysis.Hubs
{
    public class AnalysisHub : Hub<IAnalysisClient>
    {
        // The hub will be used to send updates to connected clients
        // No need to implement methods here as we'll be calling them from our endpoints
    }
}