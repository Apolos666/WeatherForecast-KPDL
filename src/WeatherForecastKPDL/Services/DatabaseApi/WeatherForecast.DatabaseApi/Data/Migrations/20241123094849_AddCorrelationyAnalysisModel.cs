using System;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Data.Migrations
{
    /// <inheritdoc />
    public partial class AddCorrelationyAnalysisModel : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CorrelationAnalyses",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("MySql:ValueGenerationStrategy", MySqlValueGenerationStrategy.IdentityColumn),
                    Date = table.Column<DateTime>(type: "datetime(6)", nullable: false),
                    TempHumidityCorrelation = table.Column<double>(type: "double", nullable: false),
                    TempPressureCorrelation = table.Column<double>(type: "double", nullable: false),
                    TempWindCorrelation = table.Column<double>(type: "double", nullable: false),
                    HumidityPressureCorrelation = table.Column<double>(type: "double", nullable: false),
                    HumidityWindCorrelation = table.Column<double>(type: "double", nullable: false),
                    PressureWindCorrelation = table.Column<double>(type: "double", nullable: false),
                    RainHumidityCorrelation = table.Column<double>(type: "double", nullable: false),
                    FeelsTempCorrelation = table.Column<double>(type: "double", nullable: false),
                    WindchillTempCorrelation = table.Column<double>(type: "double", nullable: false),
                    HeatindexTempCorrelation = table.Column<double>(type: "double", nullable: false),
                    CloudHumidityCorrelation = table.Column<double>(type: "double", nullable: false),
                    CloudWindCorrelation = table.Column<double>(type: "double", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CorrelationAnalyses", x => x.Id);
                })
                .Annotation("MySql:CharSet", "utf8mb4");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "CorrelationAnalyses");
        }
    }
}
