using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WeatherForecast.DatabaseApi.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class UpdateCentroidModel : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Year",
                table: "Centroids");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "Year",
                table: "Centroids",
                type: "int",
                nullable: false,
                defaultValue: 0);
        }
    }
}
