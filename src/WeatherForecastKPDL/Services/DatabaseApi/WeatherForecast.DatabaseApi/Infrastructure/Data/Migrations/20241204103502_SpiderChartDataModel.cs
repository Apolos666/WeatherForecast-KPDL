using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class SpiderChartDataModel : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Season",
                table: "SpiderChartDatas");

            migrationBuilder.RenameColumn(
                name: "NumberOfDays",
                table: "SpiderChartDatas",
                newName: "WinterQuantity");

            migrationBuilder.AddColumn<int>(
                name: "AutumnQuantity",
                table: "SpiderChartDatas",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "SpringQuantity",
                table: "SpiderChartDatas",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "SummerQuantity",
                table: "SpiderChartDatas",
                type: "int",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "AutumnQuantity",
                table: "SpiderChartDatas");

            migrationBuilder.DropColumn(
                name: "SpringQuantity",
                table: "SpiderChartDatas");

            migrationBuilder.DropColumn(
                name: "SummerQuantity",
                table: "SpiderChartDatas");

            migrationBuilder.RenameColumn(
                name: "WinterQuantity",
                table: "SpiderChartDatas",
                newName: "NumberOfDays");

            migrationBuilder.AddColumn<string>(
                name: "Season",
                table: "SpiderChartDatas",
                type: "longtext",
                nullable: false)
                .Annotation("MySql:CharSet", "utf8mb4");
        }
    }
}
