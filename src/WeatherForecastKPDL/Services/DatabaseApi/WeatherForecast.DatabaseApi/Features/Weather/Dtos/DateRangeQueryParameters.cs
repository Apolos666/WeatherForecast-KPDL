using Microsoft.AspNetCore.Mvc;

namespace WeatherForecast.DatabaseApi.Features.Weather.Dtos;

public class DateRangeQueryParameters
{
    [FromQuery(Name = "fromDate")] public DateTime FromDate { get; set; }

    [FromQuery(Name = "toDate")] public DateTime ToDate { get; set; }
}