using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class UpdateCorrrelationTable : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "WindchillTempCorrelation",
                table: "CorrelationAnalyses",
                newName: "WindKphTempCCorrelation");

            migrationBuilder.RenameColumn(
                name: "TempWindCorrelation",
                table: "CorrelationAnalyses",
                newName: "WindKphPressureMbCorrelation");

            migrationBuilder.RenameColumn(
                name: "TempPressureCorrelation",
                table: "CorrelationAnalyses",
                newName: "WindKphHumidityCorrelation");

            migrationBuilder.RenameColumn(
                name: "TempHumidityCorrelation",
                table: "CorrelationAnalyses",
                newName: "WindKphCloudCorrelation");

            migrationBuilder.RenameColumn(
                name: "RainHumidityCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempCWindKphCorrelation");

            migrationBuilder.RenameColumn(
                name: "PressureWindCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempCPressureMbCorrelation");

            migrationBuilder.RenameColumn(
                name: "HumidityWindCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempCHumidityCorrelation");

            migrationBuilder.RenameColumn(
                name: "HumidityPressureCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempCCloudCorrelation");

            migrationBuilder.RenameColumn(
                name: "HeatindexTempCorrelation",
                table: "CorrelationAnalyses",
                newName: "PressureMbWindKphCorrelation");

            migrationBuilder.RenameColumn(
                name: "FeelsTempCorrelation",
                table: "CorrelationAnalyses",
                newName: "PressureMbTempCCorrelation");

            migrationBuilder.RenameColumn(
                name: "Date",
                table: "CorrelationAnalyses",
                newName: "Time");

            migrationBuilder.RenameColumn(
                name: "CloudWindCorrelation",
                table: "CorrelationAnalyses",
                newName: "PressureMbHumidityCorrelation");

            migrationBuilder.AddColumn<double>(
                name: "CloudPressureMbCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "CloudTempCCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "CloudWindKphCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "HumidityCloudCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "HumidityPressureMbCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "HumidityTempCCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "HumidityWindKphCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<double>(
                name: "PressureMbCloudCorrelation",
                table: "CorrelationAnalyses",
                type: "double",
                nullable: false,
                defaultValue: 0.0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "CloudPressureMbCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "CloudTempCCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "CloudWindKphCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "HumidityCloudCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "HumidityPressureMbCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "HumidityTempCCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "HumidityWindKphCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.DropColumn(
                name: "PressureMbCloudCorrelation",
                table: "CorrelationAnalyses");

            migrationBuilder.RenameColumn(
                name: "WindKphTempCCorrelation",
                table: "CorrelationAnalyses",
                newName: "WindchillTempCorrelation");

            migrationBuilder.RenameColumn(
                name: "WindKphPressureMbCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempWindCorrelation");

            migrationBuilder.RenameColumn(
                name: "WindKphHumidityCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempPressureCorrelation");

            migrationBuilder.RenameColumn(
                name: "WindKphCloudCorrelation",
                table: "CorrelationAnalyses",
                newName: "TempHumidityCorrelation");

            migrationBuilder.RenameColumn(
                name: "Time",
                table: "CorrelationAnalyses",
                newName: "Date");

            migrationBuilder.RenameColumn(
                name: "TempCWindKphCorrelation",
                table: "CorrelationAnalyses",
                newName: "RainHumidityCorrelation");

            migrationBuilder.RenameColumn(
                name: "TempCPressureMbCorrelation",
                table: "CorrelationAnalyses",
                newName: "PressureWindCorrelation");

            migrationBuilder.RenameColumn(
                name: "TempCHumidityCorrelation",
                table: "CorrelationAnalyses",
                newName: "HumidityWindCorrelation");

            migrationBuilder.RenameColumn(
                name: "TempCCloudCorrelation",
                table: "CorrelationAnalyses",
                newName: "HumidityPressureCorrelation");

            migrationBuilder.RenameColumn(
                name: "PressureMbWindKphCorrelation",
                table: "CorrelationAnalyses",
                newName: "HeatindexTempCorrelation");

            migrationBuilder.RenameColumn(
                name: "PressureMbTempCCorrelation",
                table: "CorrelationAnalyses",
                newName: "FeelsTempCorrelation");

            migrationBuilder.RenameColumn(
                name: "PressureMbHumidityCorrelation",
                table: "CorrelationAnalyses",
                newName: "CloudWindCorrelation");
        }
    }
}
