using System;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Data.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AlterDatabase()
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Locations",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Name = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Region = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Country = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Lat = table.Column<double>(type: "double", nullable: false),
                    Lon = table.Column<double>(type: "double", nullable: false),
                    TzId = table.Column<string>(type: "varchar(50)", maxLength: 50, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    LocaltimeEpoch = table.Column<long>(type: "bigint", nullable: false),
                    Localtime = table.Column<string>(type: "varchar(50)", maxLength: 50, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Locations", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "WeatherForecasts",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    LocationId = table.Column<int>(type: "int", nullable: false),
                    Date = table.Column<DateTime>(type: "datetime(6)", nullable: false),
                    DateEpoch = table.Column<long>(type: "bigint", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_WeatherForecasts", x => x.Id);
                    table.ForeignKey(
                        name: "FK_WeatherForecasts_Locations_LocationId",
                        column: x => x.LocationId,
                        principalTable: "Locations",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Astros",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    WeatherForecastId = table.Column<int>(type: "int", nullable: false),
                    Sunrise = table.Column<string>(type: "varchar(20)", maxLength: 20, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Sunset = table.Column<string>(type: "varchar(20)", maxLength: 20, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Moonrise = table.Column<string>(type: "varchar(20)", maxLength: 20, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Moonset = table.Column<string>(type: "varchar(20)", maxLength: 20, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    MoonPhase = table.Column<string>(type: "varchar(50)", maxLength: 50, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    MoonIllumination = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Astros", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Astros_WeatherForecasts_WeatherForecastId",
                        column: x => x.WeatherForecastId,
                        principalTable: "WeatherForecasts",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Days",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    WeatherForecastId = table.Column<int>(type: "int", nullable: false),
                    MaxtempC = table.Column<double>(type: "double", nullable: false),
                    MaxtempF = table.Column<double>(type: "double", nullable: false),
                    MintempC = table.Column<double>(type: "double", nullable: false),
                    MintempF = table.Column<double>(type: "double", nullable: false),
                    AvgtempC = table.Column<double>(type: "double", nullable: false),
                    AvgtempF = table.Column<double>(type: "double", nullable: false),
                    MaxwindMph = table.Column<double>(type: "double", nullable: false),
                    MaxwindKph = table.Column<double>(type: "double", nullable: false),
                    TotalprecipMm = table.Column<double>(type: "double", nullable: false),
                    TotalprecipIn = table.Column<double>(type: "double", nullable: false),
                    TotalsnowCm = table.Column<double>(type: "double", nullable: false),
                    AvgvisKm = table.Column<double>(type: "double", nullable: false),
                    AvgvisMiles = table.Column<double>(type: "double", nullable: false),
                    Avghumidity = table.Column<int>(type: "int", nullable: false),
                    DailyWillItRain = table.Column<int>(type: "int", nullable: false),
                    DailyChanceOfRain = table.Column<int>(type: "int", nullable: false),
                    DailyWillItSnow = table.Column<int>(type: "int", nullable: false),
                    DailyChanceOfSnow = table.Column<int>(type: "int", nullable: false),
                    ConditionText = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ConditionIcon = table.Column<string>(type: "varchar(200)", maxLength: 200, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ConditionCode = table.Column<int>(type: "int", nullable: false),
                    Uv = table.Column<double>(type: "double", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Days", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Days_WeatherForecasts_WeatherForecastId",
                        column: x => x.WeatherForecastId,
                        principalTable: "WeatherForecasts",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Hours",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    WeatherForecastId = table.Column<int>(type: "int", nullable: false),
                    TimeEpoch = table.Column<long>(type: "bigint", nullable: false),
                    Time = table.Column<string>(type: "varchar(50)", maxLength: 50, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    TempC = table.Column<double>(type: "double", nullable: false),
                    TempF = table.Column<double>(type: "double", nullable: false),
                    IsDay = table.Column<int>(type: "int", nullable: false),
                    ConditionText = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ConditionIcon = table.Column<string>(type: "varchar(200)", maxLength: 200, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    ConditionCode = table.Column<int>(type: "int", nullable: false),
                    WindMph = table.Column<double>(type: "double", nullable: false),
                    WindKph = table.Column<double>(type: "double", nullable: false),
                    WindDegree = table.Column<int>(type: "int", nullable: false),
                    WindDir = table.Column<string>(type: "varchar(10)", maxLength: 10, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    PressureMb = table.Column<double>(type: "double", nullable: false),
                    PressureIn = table.Column<double>(type: "double", nullable: false),
                    PrecipMm = table.Column<double>(type: "double", nullable: false),
                    PrecipIn = table.Column<double>(type: "double", nullable: false),
                    SnowCm = table.Column<double>(type: "double", nullable: false),
                    Humidity = table.Column<int>(type: "int", nullable: false),
                    Cloud = table.Column<int>(type: "int", nullable: false),
                    FeelslikeC = table.Column<double>(type: "double", nullable: false),
                    FeelslikeF = table.Column<double>(type: "double", nullable: false),
                    WindchillC = table.Column<double>(type: "double", nullable: false),
                    WindchillF = table.Column<double>(type: "double", nullable: false),
                    HeatindexC = table.Column<double>(type: "double", nullable: false),
                    HeatindexF = table.Column<double>(type: "double", nullable: false),
                    DewpointC = table.Column<double>(type: "double", nullable: false),
                    DewpointF = table.Column<double>(type: "double", nullable: false),
                    WillItRain = table.Column<int>(type: "int", nullable: false),
                    ChanceOfRain = table.Column<int>(type: "int", nullable: false),
                    WillItSnow = table.Column<int>(type: "int", nullable: false),
                    ChanceOfSnow = table.Column<int>(type: "int", nullable: false),
                    VisKm = table.Column<double>(type: "double", nullable: false),
                    VisMiles = table.Column<double>(type: "double", nullable: false),
                    GustMph = table.Column<double>(type: "double", nullable: false),
                    GustKph = table.Column<double>(type: "double", nullable: false),
                    Uv = table.Column<double>(type: "double", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Hours", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Hours_WeatherForecasts_WeatherForecastId",
                        column: x => x.WeatherForecastId,
                        principalTable: "WeatherForecasts",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateIndex(
                name: "IX_Astros_WeatherForecastId",
                table: "Astros",
                column: "WeatherForecastId",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Days_WeatherForecastId",
                table: "Days",
                column: "WeatherForecastId",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Hours_WeatherForecastId",
                table: "Hours",
                column: "WeatherForecastId");

            migrationBuilder.CreateIndex(
                name: "IX_Locations_Name",
                table: "Locations",
                column: "Name");

            migrationBuilder.CreateIndex(
                name: "IX_WeatherForecasts_LocationId_Date",
                table: "WeatherForecasts",
                columns: new[] { "LocationId", "Date" },
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Astros");

            migrationBuilder.DropTable(
                name: "Days");

            migrationBuilder.DropTable(
                name: "Hours");

            migrationBuilder.DropTable(
                name: "WeatherForecasts");

            migrationBuilder.DropTable(
                name: "Locations");
        }
    }
}
