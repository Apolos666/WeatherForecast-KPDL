using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class UpdateSeasonalTable : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "YearMonth",
                table: "SeasonalAnalyses");

            migrationBuilder.RenameColumn(
                name: "RainyHours",
                table: "SeasonalAnalyses",
                newName: "Year");

            migrationBuilder.AlterColumn<string>(
                name: "Date",
                table: "SeasonalAnalyses",
                type: "longtext",
                nullable: false,
                oldClrType: typeof(DateTime),
                oldType: "datetime(6)")
                .Annotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.AddColumn<int>(
                name: "Quarter",
                table: "SeasonalAnalyses",
                type: "int",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Quarter",
                table: "SeasonalAnalyses");

            migrationBuilder.RenameColumn(
                name: "Year",
                table: "SeasonalAnalyses",
                newName: "RainyHours");

            migrationBuilder.AlterColumn<DateTime>(
                name: "Date",
                table: "SeasonalAnalyses",
                type: "datetime(6)",
                nullable: false,
                oldClrType: typeof(string),
                oldType: "longtext")
                .OldAnnotation("MySql:CharSet", "utf8mb4");

            migrationBuilder.AddColumn<string>(
                name: "YearMonth",
                table: "SeasonalAnalyses",
                type: "longtext",
                nullable: false)
                .Annotation("MySql:CharSet", "utf8mb4");
        }
    }
}
