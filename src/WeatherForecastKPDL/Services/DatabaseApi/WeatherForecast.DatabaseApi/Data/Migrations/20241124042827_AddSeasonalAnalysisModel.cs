using System;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Data.Migrations
{
    /// <inheritdoc />
    public partial class AddSeasonalAnalysisModel : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "SeasonalAnalyses",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Date = table.Column<DateTime>(type: "datetime(6)", nullable: false),
                    YearMonth = table.Column<string>(type: "longtext", nullable: false)
                        .Annotation("MySql:CharSet", "utf8mb4"),
                    AvgTemp = table.Column<double>(type: "double", nullable: false),
                    AvgHumidity = table.Column<double>(type: "double", nullable: false),
                    TotalPrecip = table.Column<double>(type: "double", nullable: false),
                    AvgWind = table.Column<double>(type: "double", nullable: false),
                    AvgPressure = table.Column<double>(type: "double", nullable: false),
                    MaxTemp = table.Column<double>(type: "double", nullable: false),
                    MinTemp = table.Column<double>(type: "double", nullable: false),
                    RainyHours = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_SeasonalAnalyses", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "SeasonalAnalyses");
        }
    }
}
