using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using System.IO;

namespace DoganSystem.EntityFrameworkCore
{
    public class DoganSystemDbContextFactory : IDesignTimeDbContextFactory<DoganSystemDbContext>
    {
        public DoganSystemDbContext CreateDbContext(string[] args)
        {
            var configuration = BuildConfiguration();

            var builder = new DbContextOptionsBuilder<DoganSystemDbContext>()
                .UseNpgsql(configuration.GetConnectionString("Default"));

            return new DoganSystemDbContext(builder.Options);
        }

        private static IConfigurationRoot BuildConfiguration()
        {
            var builder = new ConfigurationBuilder()
                .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), "../DoganSystem.Web.Mvc"))
                .AddJsonFile("appsettings.json", optional: false);

            return builder.Build();
        }
    }
}
