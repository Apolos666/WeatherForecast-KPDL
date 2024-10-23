using Mapster;
using WeatherForecast.DatabaseApi.Dtos;
using WeatherForecast.DatabaseApi.Entities;

namespace WeatherForecast.DatabaseApi.Configurations
{
    public static class MapsterConfig
    {
        public static void RegisterMaps(TypeAdapterConfig config)
        {
            config.NewConfig<WeatherDataDto, WeatherData>()
                .Map(dest => dest.Location, src => src.Location)
                .Map(dest => dest.Current, src => src.Current);

            config.NewConfig<LocationDto, Location>()
                .MapToConstructor(true);

            config.NewConfig<CurrentDto, Current>()
                .MapToConstructor(true)
                .Map(dest => dest.Condition, src => src.Condition);

            config.NewConfig<ConditionDto, Condition>()
                .MapToConstructor(true);
        }
    }
}
