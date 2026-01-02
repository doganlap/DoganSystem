using DoganSystem.Permissions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace DoganSystem.Web.Mvc.Menus;

public static class GrcMenuHelper
{
    public static bool CanAccess(IAuthorizationService authorizationService, ClaimsPrincipal user, string permission)
    {
        return authorizationService.AuthorizeAsync(user, null, permission).Result.Succeeded;
    }
}
