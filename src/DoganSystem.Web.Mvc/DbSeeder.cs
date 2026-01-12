using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using DoganSystem.EntityFrameworkCore;

namespace DoganSystem.Web.Mvc;

/// <summary>
/// Direct database seeder using raw SQL to bypass ABP's repository abstraction
/// and work around the CurrentTenant null reference issue during initialization.
/// </summary>
public static class DbSeeder
{
    public static async Task SeedAsync(IServiceProvider serviceProvider)
    {
        Console.WriteLine("Starting direct database seeding...");

        try
        {
            using var scope = serviceProvider.CreateScope();
            var dbContext = scope.ServiceProvider.GetRequiredService<DoganSystemDbContext>();
            var connection = dbContext.Database.GetDbConnection();

            await connection.OpenAsync();

            try
            {
                using var cmd = connection.CreateCommand();

                // Check if admin role exists
                cmd.CommandText = "SELECT COUNT(*) FROM AbpRoles WHERE NormalizedName = 'ADMIN'";
                var adminRoleCount = Convert.ToInt32(await cmd.ExecuteScalarAsync());

                if (adminRoleCount == 0)
                {
                    Console.WriteLine("Creating admin role...");
                    cmd.CommandText = @"
                        INSERT INTO AbpRoles (Id, TenantId, Name, NormalizedName, IsDefault, IsStatic, IsPublic, EntityVersion, ExtraProperties, ConcurrencyStamp)
                        VALUES (@id, NULL, 'admin', 'ADMIN', 0, 1, 1, 0, '{}', @stamp)";
                    cmd.Parameters.Clear();
                    AddParameter(cmd, "@id", Guid.NewGuid().ToString());
                    AddParameter(cmd, "@stamp", Guid.NewGuid().ToString());
                    await cmd.ExecuteNonQueryAsync();
                    Console.WriteLine("Admin role created.");
                }
                else
                {
                    Console.WriteLine("Admin role already exists.");
                }

                // Check if user role exists
                cmd.CommandText = "SELECT COUNT(*) FROM AbpRoles WHERE NormalizedName = 'USER'";
                cmd.Parameters.Clear();
                var userRoleCount = Convert.ToInt32(await cmd.ExecuteScalarAsync());

                if (userRoleCount == 0)
                {
                    Console.WriteLine("Creating user role...");
                    cmd.CommandText = @"
                        INSERT INTO AbpRoles (Id, TenantId, Name, NormalizedName, IsDefault, IsStatic, IsPublic, EntityVersion, ExtraProperties, ConcurrencyStamp)
                        VALUES (@id, NULL, 'user', 'USER', 1, 1, 1, 0, '{}', @stamp)";
                    cmd.Parameters.Clear();
                    AddParameter(cmd, "@id", Guid.NewGuid().ToString());
                    AddParameter(cmd, "@stamp", Guid.NewGuid().ToString());
                    await cmd.ExecuteNonQueryAsync();
                    Console.WriteLine("User role created.");
                }
                else
                {
                    Console.WriteLine("User role already exists.");
                }

                // Create admin user with hashed password
                const string adminEmail = "admin@saudibusinessgate.com";
                const string adminUserName = "admin";

                cmd.CommandText = "SELECT COUNT(*) FROM AbpUsers WHERE NormalizedEmail = @email";
                cmd.Parameters.Clear();
                AddParameter(cmd, "@email", adminEmail.ToUpperInvariant());
                var adminUserCount = Convert.ToInt32(await cmd.ExecuteScalarAsync());

                if (adminUserCount == 0)
                {
                    Console.WriteLine("Creating admin user...");
                    var passwordHash = HashPassword("Admin123!");
                    var userId = Guid.NewGuid().ToString();
                    var now = DateTime.UtcNow.ToString("o");

                    cmd.CommandText = @"
                        INSERT INTO AbpUsers (
                            Id, TenantId, UserName, NormalizedUserName, Name, Surname,
                            Email, NormalizedEmail, EmailConfirmed, PasswordHash,
                            SecurityStamp, IsExternal, PhoneNumberConfirmed, IsActive,
                            TwoFactorEnabled, LockoutEnabled, AccessFailedCount,
                            ShouldChangePasswordOnNextLogin, EntityVersion,
                            ExtraProperties, ConcurrencyStamp, CreationTime, IsDeleted
                        )
                        VALUES (
                            @id, NULL, @userName, @normalizedUserName, @name, @surname,
                            @email, @normalizedEmail, 1, @passwordHash,
                            @securityStamp, 0, 0, 1,
                            0, 1, 0,
                            0, 0,
                            '{}', @concurrencyStamp, @creationTime, 0
                        )";
                    cmd.Parameters.Clear();
                    AddParameter(cmd, "@id", userId);
                    AddParameter(cmd, "@userName", adminUserName);
                    AddParameter(cmd, "@normalizedUserName", adminUserName.ToUpperInvariant());
                    AddParameter(cmd, "@name", "System");
                    AddParameter(cmd, "@surname", "Administrator");
                    AddParameter(cmd, "@email", adminEmail);
                    AddParameter(cmd, "@normalizedEmail", adminEmail.ToUpperInvariant());
                    AddParameter(cmd, "@passwordHash", passwordHash);
                    AddParameter(cmd, "@securityStamp", Guid.NewGuid().ToString());
                    AddParameter(cmd, "@concurrencyStamp", Guid.NewGuid().ToString());
                    AddParameter(cmd, "@creationTime", now);
                    await cmd.ExecuteNonQueryAsync();
                    Console.WriteLine($"Admin user created: {adminEmail}");

                    // Assign admin role to admin user
                    cmd.CommandText = @"
                        INSERT INTO AbpUserRoles (UserId, RoleId, TenantId)
                        SELECT @userId, r.Id, NULL
                        FROM AbpRoles r
                        WHERE r.NormalizedName = 'ADMIN'";
                    cmd.Parameters.Clear();
                    AddParameter(cmd, "@userId", userId);
                    await cmd.ExecuteNonQueryAsync();
                    Console.WriteLine("Admin role assigned to admin user.");
                }
                else
                {
                    Console.WriteLine($"Admin user already exists: {adminEmail}");
                }

                Console.WriteLine("Database seeding completed successfully.");
            }
            finally
            {
                await connection.CloseAsync();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error during database seeding: {ex.Message}");
            Console.WriteLine($"Stack trace: {ex.StackTrace}");
            // Don't throw - let the app continue even if seeding fails
        }
    }

    private static void AddParameter(System.Data.Common.DbCommand cmd, string name, object value)
    {
        var param = cmd.CreateParameter();
        param.ParameterName = name;
        param.Value = value ?? DBNull.Value;
        cmd.Parameters.Add(param);
    }

    private static string HashPassword(string password)
    {
        var hasher = new Microsoft.AspNetCore.Identity.PasswordHasher<object>();
        return hasher.HashPassword(null!, password);
    }
}
