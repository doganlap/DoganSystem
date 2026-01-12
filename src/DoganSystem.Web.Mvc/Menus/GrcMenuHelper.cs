using DoganSystem.Permissions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace DoganSystem.Web.Mvc.Menus;

public static class GrcMenuHelper
{
    public static bool CanAccess(IAuthorizationService authorizationService, ClaimsPrincipal user, string permission)
    {
        return authorizationService.AuthorizeAsync(user, null, permission).GetAwaiter().GetResult().Succeeded;
    }

    public static async Task<bool> CanAccessAsync(IAuthorizationService authorizationService, ClaimsPrincipal user, string permission)
    {
        var result = await authorizationService.AuthorizeAsync(user, null, permission);
        return result.Succeeded;
    }
}
