using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.IdentityModel.Tokens;
using Volo.Abp.Identity;
using OtpNet;

namespace DoganSystem.Web.Mvc.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly IdentityUserManager _userManager;
        private readonly IdentityRoleManager _roleManager;
        private readonly SignInManager<Volo.Abp.Identity.IdentityUser> _signInManager;
        private readonly IConfiguration _configuration;
        private readonly IMemoryCache _cache;

        // In-memory stores (use Redis/DB in production)
        private static readonly Dictionary<string, RefreshTokenInfo> _refreshTokens = new();
        private static readonly Dictionary<string, List<SessionInfo>> _userSessions = new();
        private static readonly Dictionary<string, string> _passwordResetTokens = new();
        private static readonly Dictionary<string, TwoFactorInfo> _twoFactorSecrets = new();

        public AuthController(
            IdentityUserManager userManager,
            IdentityRoleManager roleManager,
            SignInManager<Volo.Abp.Identity.IdentityUser> signInManager,
            IConfiguration configuration,
            IMemoryCache cache)
        {
            _userManager = userManager;
            _roleManager = roleManager;
            _signInManager = signInManager;
            _configuration = configuration;
            _cache = cache;
        }

        #region Login & Logout

        [HttpPost("login")]
        [AllowAnonymous]
        public async Task<IActionResult> Login([FromBody] LoginDto input)
        {
            if (string.IsNullOrEmpty(input.UserNameOrEmail) || string.IsNullOrEmpty(input.Password))
            {
                return BadRequest(new { error = "Username and password are required" });
            }

            var user = await _userManager.FindByNameAsync(input.UserNameOrEmail)
                       ?? await _userManager.FindByEmailAsync(input.UserNameOrEmail);

            if (user == null)
            {
                return Unauthorized(new { error = "Invalid username or password" });
            }

            var result = await _signInManager.CheckPasswordSignInAsync(user, input.Password, lockoutOnFailure: true);

            if (result.IsLockedOut)
            {
                return Unauthorized(new { error = "Account is locked. Please try again later." });
            }

            if (!result.Succeeded)
            {
                return Unauthorized(new { error = "Invalid username or password" });
            }

            // Check if 2FA is enabled
            if (_twoFactorSecrets.TryGetValue(user.Id.ToString(), out var twoFactorInfo) && twoFactorInfo.IsEnabled)
            {
                if (string.IsNullOrEmpty(input.TwoFactorCode))
                {
                    return Ok(new { requiresTwoFactor = true, message = "Please provide 2FA code" });
                }

                if (!VerifyTwoFactorCode(user.Id.ToString(), input.TwoFactorCode))
                {
                    return Unauthorized(new { error = "Invalid 2FA code" });
                }
            }

            // Generate tokens
            var accessToken = await GenerateJwtToken(user);
            var refreshToken = GenerateRefreshToken();
            var roles = await _userManager.GetRolesAsync(user);

            // Store refresh token
            var expiresAt = input.RememberMe ? DateTime.UtcNow.AddDays(30) : DateTime.UtcNow.AddDays(7);
            _refreshTokens[refreshToken] = new RefreshTokenInfo
            {
                UserId = user.Id.ToString(),
                ExpiresAt = expiresAt,
                CreatedAt = DateTime.UtcNow,
                DeviceInfo = Request.Headers["User-Agent"].ToString()
            };

            // Create session
            var sessionId = Guid.NewGuid().ToString();
            var session = new SessionInfo
            {
                SessionId = sessionId,
                DeviceInfo = Request.Headers["User-Agent"].ToString(),
                IpAddress = HttpContext.Connection.RemoteIpAddress?.ToString() ?? "Unknown",
                CreatedAt = DateTime.UtcNow,
                LastActivity = DateTime.UtcNow,
                IsActive = true
            };

            if (!_userSessions.ContainsKey(user.Id.ToString()))
            {
                _userSessions[user.Id.ToString()] = new List<SessionInfo>();
            }
            _userSessions[user.Id.ToString()].Add(session);

            return Ok(new LoginResultDto
            {
                AccessToken = accessToken,
                RefreshToken = refreshToken,
                TokenType = "Bearer",
                ExpiresIn = 3600, // 1 hour
                RefreshExpiresIn = input.RememberMe ? 2592000 : 604800, // 30 or 7 days
                UserId = user.Id.ToString(),
                UserName = user.UserName,
                Email = user.Email,
                Name = user.Name ?? user.UserName,
                Roles = roles.ToList(),
                TwoFactorEnabled = _twoFactorSecrets.TryGetValue(user.Id.ToString(), out var tf) && tf.IsEnabled,
                SessionId = sessionId
            });
        }

        [HttpPost("logout")]
        [Authorize]
        public IActionResult Logout([FromBody] LogoutDto input)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

            // Remove refresh token
            if (!string.IsNullOrEmpty(input.RefreshToken) && _refreshTokens.ContainsKey(input.RefreshToken))
            {
                _refreshTokens.Remove(input.RefreshToken);
            }

            // Deactivate session
            if (!string.IsNullOrEmpty(input.SessionId) && _userSessions.TryGetValue(userId, out var sessions))
            {
                var session = sessions.FirstOrDefault(s => s.SessionId == input.SessionId);
                if (session != null)
                {
                    session.IsActive = false;
                }
            }

            return Ok(new { message = "Logged out successfully" });
        }

        #endregion

        #region Refresh Token

        [HttpPost("refresh-token")]
        [AllowAnonymous]
        public async Task<IActionResult> RefreshToken([FromBody] RefreshTokenDto input)
        {
            if (string.IsNullOrEmpty(input.RefreshToken))
            {
                return BadRequest(new { error = "Refresh token is required" });
            }

            if (!_refreshTokens.TryGetValue(input.RefreshToken, out var tokenInfo))
            {
                return Unauthorized(new { error = "Invalid refresh token" });
            }

            if (tokenInfo.ExpiresAt < DateTime.UtcNow)
            {
                _refreshTokens.Remove(input.RefreshToken);
                return Unauthorized(new { error = "Refresh token expired" });
            }

            var user = await _userManager.FindByIdAsync(tokenInfo.UserId);
            if (user == null)
            {
                return Unauthorized(new { error = "User not found" });
            }

            // Generate new tokens
            var newAccessToken = await GenerateJwtToken(user);
            var newRefreshToken = GenerateRefreshToken();
            var roles = await _userManager.GetRolesAsync(user);

            // Rotate refresh token (invalidate old, create new)
            _refreshTokens.Remove(input.RefreshToken);
            _refreshTokens[newRefreshToken] = new RefreshTokenInfo
            {
                UserId = user.Id.ToString(),
                ExpiresAt = tokenInfo.ExpiresAt, // Keep same expiry
                CreatedAt = DateTime.UtcNow,
                DeviceInfo = tokenInfo.DeviceInfo
            };

            return Ok(new LoginResultDto
            {
                AccessToken = newAccessToken,
                RefreshToken = newRefreshToken,
                TokenType = "Bearer",
                ExpiresIn = 3600,
                RefreshExpiresIn = (int)(tokenInfo.ExpiresAt - DateTime.UtcNow).TotalSeconds,
                UserId = user.Id.ToString(),
                UserName = user.UserName,
                Email = user.Email,
                Name = user.Name ?? user.UserName,
                Roles = roles.ToList(),
                TwoFactorEnabled = _twoFactorSecrets.TryGetValue(user.Id.ToString(), out var tf) && tf.IsEnabled
            });
        }

        #endregion

        #region Password Reset

        [HttpPost("forgot-password")]
        [AllowAnonymous]
        public async Task<IActionResult> ForgotPassword([FromBody] ForgotPasswordDto input)
        {
            var user = await _userManager.FindByEmailAsync(input.Email);
            if (user == null)
            {
                // Don't reveal if user exists
                return Ok(new { message = "If the email exists, a reset link has been sent" });
            }

            // Generate reset token
            var resetToken = GenerateSecureToken();
            _passwordResetTokens[resetToken] = user.Id.ToString();

            // In production, send email here
            // For now, return token directly (REMOVE IN PRODUCTION)
            return Ok(new
            {
                message = "If the email exists, a reset link has been sent",
                // DEVELOPMENT ONLY - Remove in production
                devResetToken = resetToken,
                devResetUrl = $"/reset-password?token={resetToken}"
            });
        }

        [HttpPost("reset-password")]
        [AllowAnonymous]
        public async Task<IActionResult> ResetPassword([FromBody] ResetPasswordDto input)
        {
            if (!_passwordResetTokens.TryGetValue(input.Token, out var userId))
            {
                return BadRequest(new { error = "Invalid or expired reset token" });
            }

            var user = await _userManager.FindByIdAsync(userId);
            if (user == null)
            {
                return BadRequest(new { error = "User not found" });
            }

            // Reset password using ABP Identity
            var token = await _userManager.GeneratePasswordResetTokenAsync(user);
            var result = await _userManager.ResetPasswordAsync(user, token, input.NewPassword);

            if (!result.Succeeded)
            {
                var errors = string.Join(", ", result.Errors.Select(e => e.Description));
                return BadRequest(new { error = $"Failed to reset password: {errors}" });
            }

            // Remove used token
            _passwordResetTokens.Remove(input.Token);

            // Invalidate all refresh tokens for this user
            var tokensToRemove = _refreshTokens.Where(t => t.Value.UserId == userId).Select(t => t.Key).ToList();
            foreach (var tokenKey in tokensToRemove)
            {
                _refreshTokens.Remove(tokenKey);
            }

            return Ok(new { message = "Password reset successfully. Please login with your new password." });
        }

        #endregion

        #region Two-Factor Authentication

        [HttpPost("2fa/setup")]
        [Authorize]
        public IActionResult SetupTwoFactor()
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var userName = User.FindFirstValue(ClaimTypes.Name);

            // Generate secret key
            var secret = KeyGeneration.GenerateRandomKey(20);
            var base32Secret = Base32Encoding.ToString(secret);

            // Store temporarily (not enabled yet)
            _twoFactorSecrets[userId] = new TwoFactorInfo
            {
                Secret = base32Secret,
                IsEnabled = false,
                SetupAt = DateTime.UtcNow
            };

            // Generate QR code URI for authenticator apps
            var issuer = "DoganSystem";
            var otpUri = $"otpauth://totp/{issuer}:{userName}?secret={base32Secret}&issuer={issuer}&algorithm=SHA1&digits=6&period=30";

            return Ok(new
            {
                secret = base32Secret,
                qrCodeUri = otpUri,
                message = "Scan the QR code with your authenticator app, then verify with a code"
            });
        }

        [HttpPost("2fa/verify-setup")]
        [Authorize]
        public IActionResult VerifyTwoFactorSetup([FromBody] TwoFactorVerifyDto input)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

            if (!_twoFactorSecrets.TryGetValue(userId, out var twoFactorInfo))
            {
                return BadRequest(new { error = "Please setup 2FA first" });
            }

            if (!VerifyTwoFactorCode(userId, input.Code))
            {
                return BadRequest(new { error = "Invalid verification code" });
            }

            // Enable 2FA
            twoFactorInfo.IsEnabled = true;
            twoFactorInfo.EnabledAt = DateTime.UtcNow;

            // Generate backup codes
            var backupCodes = GenerateBackupCodes();
            twoFactorInfo.BackupCodes = backupCodes;

            return Ok(new
            {
                message = "Two-factor authentication enabled successfully",
                backupCodes = backupCodes,
                warning = "Save these backup codes securely. They can only be used once."
            });
        }

        [HttpPost("2fa/disable")]
        [Authorize]
        public IActionResult DisableTwoFactor([FromBody] TwoFactorVerifyDto input)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

            if (!_twoFactorSecrets.TryGetValue(userId, out var twoFactorInfo) || !twoFactorInfo.IsEnabled)
            {
                return BadRequest(new { error = "2FA is not enabled" });
            }

            if (!VerifyTwoFactorCode(userId, input.Code))
            {
                return BadRequest(new { error = "Invalid verification code" });
            }

            _twoFactorSecrets.Remove(userId);

            return Ok(new { message = "Two-factor authentication disabled" });
        }

        [HttpGet("2fa/status")]
        [Authorize]
        public IActionResult GetTwoFactorStatus()
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var isEnabled = _twoFactorSecrets.TryGetValue(userId, out var tf) && tf.IsEnabled;

            return Ok(new
            {
                enabled = isEnabled,
                enabledAt = isEnabled ? tf?.EnabledAt : null
            });
        }

        #endregion

        #region Session Management

        [HttpGet("sessions")]
        [Authorize]
        public IActionResult GetSessions()
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

            if (!_userSessions.TryGetValue(userId, out var sessions))
            {
                return Ok(new { sessions = new List<object>() });
            }

            var activeSessions = sessions
                .Where(s => s.IsActive)
                .Select(s => new
                {
                    s.SessionId,
                    s.DeviceInfo,
                    s.IpAddress,
                    s.CreatedAt,
                    s.LastActivity,
                    isCurrent = s.SessionId == Request.Headers["X-Session-Id"].ToString()
                })
                .ToList();

            return Ok(new { sessions = activeSessions });
        }

        [HttpPost("sessions/{sessionId}/revoke")]
        [Authorize]
        public IActionResult RevokeSession(string sessionId)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

            if (!_userSessions.TryGetValue(userId, out var sessions))
            {
                return NotFound(new { error = "Session not found" });
            }

            var session = sessions.FirstOrDefault(s => s.SessionId == sessionId);
            if (session == null)
            {
                return NotFound(new { error = "Session not found" });
            }

            session.IsActive = false;

            // Also revoke associated refresh tokens
            var tokensToRemove = _refreshTokens
                .Where(t => t.Value.UserId == userId && t.Value.DeviceInfo == session.DeviceInfo)
                .Select(t => t.Key)
                .ToList();

            foreach (var token in tokensToRemove)
            {
                _refreshTokens.Remove(token);
            }

            return Ok(new { message = "Session revoked successfully" });
        }

        [HttpPost("sessions/revoke-all")]
        [Authorize]
        public IActionResult RevokeAllSessions()
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var currentSessionId = Request.Headers["X-Session-Id"].ToString();

            if (_userSessions.TryGetValue(userId, out var sessions))
            {
                foreach (var session in sessions)
                {
                    if (session.SessionId != currentSessionId)
                    {
                        session.IsActive = false;
                    }
                }
            }

            // Revoke all refresh tokens except current
            var tokensToRemove = _refreshTokens
                .Where(t => t.Value.UserId == userId)
                .Select(t => t.Key)
                .ToList();

            foreach (var token in tokensToRemove)
            {
                _refreshTokens.Remove(token);
            }

            return Ok(new { message = "All other sessions revoked" });
        }

        #endregion

        #region Role-Based Access

        [HttpGet("me")]
        [Authorize]
        public async Task<IActionResult> GetCurrentUser()
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            if (string.IsNullOrEmpty(userId))
            {
                return Unauthorized();
            }

            var user = await _userManager.FindByIdAsync(userId);
            if (user == null)
            {
                return NotFound();
            }

            var roles = await _userManager.GetRolesAsync(user);
            var permissions = new List<string>();

            // Get permissions from roles
            foreach (var roleName in roles)
            {
                if (roleName == "admin")
                {
                    permissions.AddRange(new[] { "users.read", "users.write", "users.delete", "settings.manage", "reports.view" });
                }
                else if (roleName == "manager")
                {
                    permissions.AddRange(new[] { "users.read", "reports.view" });
                }
                else
                {
                    permissions.Add("self.read");
                }
            }

            return Ok(new UserInfoDto
            {
                UserId = user.Id.ToString(),
                UserName = user.UserName,
                Email = user.Email,
                Name = user.Name ?? user.UserName,
                Roles = roles.ToList(),
                Permissions = permissions.Distinct().ToList(),
                TwoFactorEnabled = _twoFactorSecrets.TryGetValue(userId, out var tf) && tf.IsEnabled
            });
        }

        [HttpGet("users")]
        [Authorize(Roles = "admin")]
        public async Task<IActionResult> GetUsers()
        {
            var users = _userManager.Users.Take(100).ToList();
            var result = new List<object>();

            foreach (var user in users)
            {
                var roles = await _userManager.GetRolesAsync(user);
                result.Add(new
                {
                    userId = user.Id.ToString(),
                    userName = user.UserName,
                    email = user.Email,
                    name = user.Name,
                    roles = roles,
                    creationTime = user.CreationTime,
                    isActive = user.IsActive
                });
            }

            return Ok(new { users = result });
        }

        [HttpPost("users/{userId}/roles")]
        [Authorize(Roles = "admin")]
        public async Task<IActionResult> AssignRole(string userId, [FromBody] AssignRoleDto input)
        {
            var user = await _userManager.FindByIdAsync(userId);
            if (user == null)
            {
                return NotFound(new { error = "User not found" });
            }

            // Check if role exists
            var roleExists = await _roleManager.RoleExistsAsync(input.Role);
            if (!roleExists)
            {
                return BadRequest(new { error = "Role does not exist" });
            }

            var result = await _userManager.AddToRoleAsync(user, input.Role);
            if (!result.Succeeded)
            {
                return BadRequest(new { error = "Failed to assign role" });
            }

            return Ok(new { message = $"Role '{input.Role}' assigned to user" });
        }

        [HttpDelete("users/{userId}/roles/{role}")]
        [Authorize(Roles = "admin")]
        public async Task<IActionResult> RemoveRole(string userId, string role)
        {
            var user = await _userManager.FindByIdAsync(userId);
            if (user == null)
            {
                return NotFound(new { error = "User not found" });
            }

            var result = await _userManager.RemoveFromRoleAsync(user, role);
            if (!result.Succeeded)
            {
                return BadRequest(new { error = "Failed to remove role" });
            }

            return Ok(new { message = $"Role '{role}' removed from user" });
        }

        [HttpPost("change-password")]
        [Authorize]
        public async Task<IActionResult> ChangePassword([FromBody] ChangePasswordDto input)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var user = await _userManager.FindByIdAsync(userId);

            if (user == null)
            {
                return NotFound();
            }

            var result = await _userManager.ChangePasswordAsync(user, input.CurrentPassword, input.NewPassword);

            if (!result.Succeeded)
            {
                var errors = string.Join(", ", result.Errors.Select(e => e.Description));
                return BadRequest(new { error = $"Failed to change password: {errors}" });
            }

            return Ok(new { message = "Password changed successfully" });
        }

        [HttpPost("register")]
        [Authorize(Roles = "admin")]
        public async Task<IActionResult> Register([FromBody] RegisterDto input)
        {
            if (string.IsNullOrEmpty(input.UserName) || string.IsNullOrEmpty(input.Email) || string.IsNullOrEmpty(input.Password))
            {
                return BadRequest(new { error = "All fields are required" });
            }

            var existingUser = await _userManager.FindByNameAsync(input.UserName);
            if (existingUser != null)
            {
                return BadRequest(new { error = "Username already taken" });
            }

            existingUser = await _userManager.FindByEmailAsync(input.Email);
            if (existingUser != null)
            {
                return BadRequest(new { error = "Email already registered" });
            }

            var user = new Volo.Abp.Identity.IdentityUser(Guid.NewGuid(), input.UserName, input.Email)
            {
                Name = input.Name ?? input.UserName
            };

            var result = await _userManager.CreateAsync(user, input.Password);

            if (!result.Succeeded)
            {
                var errors = string.Join(", ", result.Errors.Select(e => e.Description));
                return BadRequest(new { error = $"Failed to create user: {errors}" });
            }

            // Assign default role
            if (!string.IsNullOrEmpty(input.Role))
            {
                await _userManager.AddToRoleAsync(user, input.Role);
            }

            return Ok(new
            {
                userId = user.Id.ToString(),
                userName = user.UserName,
                email = user.Email,
                message = "User created successfully"
            });
        }

        #endregion

        #region Helper Methods

        private async Task<string> GenerateJwtToken(Volo.Abp.Identity.IdentityUser user)
        {
            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.UserName),
                new Claim(ClaimTypes.Email, user.Email ?? ""),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString())
            };

            var roles = await _userManager.GetRolesAsync(user);
            foreach (var role in roles)
            {
                claims.Add(new Claim(ClaimTypes.Role, role));
            }

            var secretKey = _configuration["Jwt:SecretKey"] ?? "DoganSystem_SuperSecret_Key_2026_Must_Be_At_Least_32_Characters_Long!";
            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"] ?? "DoganSystem",
                audience: _configuration["Jwt:Audience"] ?? "DoganSystem",
                claims: claims,
                expires: DateTime.UtcNow.AddHours(1), // Short-lived access token
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        private string GenerateRefreshToken()
        {
            var randomBytes = new byte[64];
            using var rng = RandomNumberGenerator.Create();
            rng.GetBytes(randomBytes);
            return Convert.ToBase64String(randomBytes);
        }

        private string GenerateSecureToken()
        {
            var randomBytes = new byte[32];
            using var rng = RandomNumberGenerator.Create();
            rng.GetBytes(randomBytes);
            return Convert.ToHexString(randomBytes).ToLower();
        }

        private bool VerifyTwoFactorCode(string userId, string code)
        {
            if (!_twoFactorSecrets.TryGetValue(userId, out var twoFactorInfo))
            {
                return false;
            }

            // Check backup codes first
            if (twoFactorInfo.BackupCodes != null && twoFactorInfo.BackupCodes.Contains(code))
            {
                twoFactorInfo.BackupCodes.Remove(code);
                return true;
            }

            // Verify TOTP
            var secretBytes = Base32Encoding.ToBytes(twoFactorInfo.Secret);
            var totp = new Totp(secretBytes);
            return totp.VerifyTotp(code, out _, new VerificationWindow(1, 1));
        }

        private List<string> GenerateBackupCodes()
        {
            var codes = new List<string>();
            using var rng = RandomNumberGenerator.Create();

            for (int i = 0; i < 10; i++)
            {
                var bytes = new byte[4];
                rng.GetBytes(bytes);
                var code = (BitConverter.ToUInt32(bytes, 0) % 100000000).ToString("D8");
                codes.Add($"{code.Substring(0, 4)}-{code.Substring(4, 4)}");
            }

            return codes;
        }

        #endregion
    }

    #region DTOs

    public class LoginDto
    {
        public string UserNameOrEmail { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public bool RememberMe { get; set; }
        public string? TwoFactorCode { get; set; }
    }

    public class LogoutDto
    {
        public string? RefreshToken { get; set; }
        public string? SessionId { get; set; }
    }

    public class RefreshTokenDto
    {
        public string RefreshToken { get; set; } = string.Empty;
    }

    public class RegisterDto
    {
        public string UserName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public string? Name { get; set; }
        public string? Role { get; set; }
    }

    public class LoginResultDto
    {
        public string AccessToken { get; set; } = string.Empty;
        public string RefreshToken { get; set; } = string.Empty;
        public string TokenType { get; set; } = "Bearer";
        public int ExpiresIn { get; set; }
        public int RefreshExpiresIn { get; set; }
        public string UserId { get; set; } = string.Empty;
        public string UserName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public List<string> Roles { get; set; } = new();
        public bool TwoFactorEnabled { get; set; }
        public string? SessionId { get; set; }
    }

    public class UserInfoDto
    {
        public string UserId { get; set; } = string.Empty;
        public string UserName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public List<string> Roles { get; set; } = new();
        public List<string> Permissions { get; set; } = new();
        public bool TwoFactorEnabled { get; set; }
    }

    public class ChangePasswordDto
    {
        public string CurrentPassword { get; set; } = string.Empty;
        public string NewPassword { get; set; } = string.Empty;
    }

    public class ForgotPasswordDto
    {
        public string Email { get; set; } = string.Empty;
    }

    public class ResetPasswordDto
    {
        public string Token { get; set; } = string.Empty;
        public string NewPassword { get; set; } = string.Empty;
    }

    public class TwoFactorVerifyDto
    {
        public string Code { get; set; } = string.Empty;
    }

    public class AssignRoleDto
    {
        public string Role { get; set; } = string.Empty;
    }

    // Internal models
    public class RefreshTokenInfo
    {
        public string UserId { get; set; } = string.Empty;
        public DateTime ExpiresAt { get; set; }
        public DateTime CreatedAt { get; set; }
        public string DeviceInfo { get; set; } = string.Empty;
    }

    public class SessionInfo
    {
        public string SessionId { get; set; } = string.Empty;
        public string DeviceInfo { get; set; } = string.Empty;
        public string IpAddress { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
        public DateTime LastActivity { get; set; }
        public bool IsActive { get; set; }
    }

    public class TwoFactorInfo
    {
        public string Secret { get; set; } = string.Empty;
        public bool IsEnabled { get; set; }
        public DateTime SetupAt { get; set; }
        public DateTime? EnabledAt { get; set; }
        public List<string>? BackupCodes { get; set; }
    }

    #endregion
}
