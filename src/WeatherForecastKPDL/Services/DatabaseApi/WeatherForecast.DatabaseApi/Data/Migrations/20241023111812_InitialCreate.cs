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
                name: "Conditions",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Text = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Icon = table.Column<string>(type: "varchar(200)", maxLength: 200, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Code = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Conditions", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "Locations",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Name = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Country = table.Column<string>(type: "varchar(100)", maxLength: 100, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    Localtime = table.Column<string>(type: "varchar(50)", maxLength: 50, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Locations", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "CurrentWeather",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    LastUpdated = table.Column<string>(type: "varchar(50)", maxLength: 50, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    TempC = table.Column<double>(type: "double", nullable: false),
                    TempF = table.Column<double>(type: "double", nullable: false),
                    IsDay = table.Column<int>(type: "int", nullable: false),
                    ConditionId = table.Column<int>(type: "int", nullable: false),
                    WindMph = table.Column<double>(type: "double", nullable: false),
                    WindKph = table.Column<double>(type: "double", nullable: false),
                    WindDegree = table.Column<int>(type: "int", nullable: false),
                    WindDir = table.Column<string>(type: "varchar(10)", maxLength: 10, nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    PressureMb = table.Column<double>(type: "double", nullable: false),
                    PressureIn = table.Column<double>(type: "double", nullable: false),
                    PrecipMm = table.Column<double>(type: "double", nullable: false),
                    PrecipIn = table.Column<double>(type: "double", nullable: false),
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
                    VisKm = table.Column<double>(type: "double", nullable: false),
                    VisMiles = table.Column<double>(type: "double", nullable: false),
                    Uv = table.Column<double>(type: "double", nullable: false),
                    GustMph = table.Column<double>(type: "double", nullable: false),
                    GustKph = table.Column<double>(type: "double", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CurrentWeather", x => x.Id);
                    table.ForeignKey(
                        name: "FK_CurrentWeather_Conditions_ConditionId",
                        column: x => x.ConditionId,
                        principalTable: "Conditions",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateTable(
                name: "WeatherData",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    LocationId = table.Column<int>(type: "int", nullable: false),
                    CurrentId = table.Column<int>(type: "int", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime(6)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_WeatherData", x => x.Id);
                    table.ForeignKey(
                        name: "FK_WeatherData_CurrentWeather_CurrentId",
                        column: x => x.CurrentId,
                        principalTable: "CurrentWeather",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_WeatherData_Locations_LocationId",
                        column: x => x.LocationId,
                        principalTable: "Locations",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                })
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.CreateIndex(
                name: "IX_CurrentWeather_ConditionId",
                table: "CurrentWeather",
                column: "ConditionId");

            migrationBuilder.CreateIndex(
                name: "IX_WeatherData_CurrentId",
                table: "WeatherData",
                column: "CurrentId");

            migrationBuilder.CreateIndex(
                name: "IX_WeatherData_LocationId",
                table: "WeatherData",
                column: "LocationId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "WeatherData");

            migrationBuilder.DropTable(
                name: "CurrentWeather");

            migrationBuilder.DropTable(
                name: "Locations");

            migrationBuilder.DropTable(
                name: "Conditions");
        }
    }
}
