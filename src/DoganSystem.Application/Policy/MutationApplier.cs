using System.Text.Json;
using DoganSystem.Application.Policy.PolicyModels;

namespace DoganSystem.Application.Policy;

public class MutationApplier
{
    public static void ApplyMutation(object resource, PolicyMutation mutation)
    {
        var value = ResolveValue(resource, mutation.Path);
        var parentPath = GetParentPath(mutation.Path);
        var propertyName = GetPropertyName(mutation.Path);

        switch (mutation.Op.ToLower())
        {
            case "set":
                SetValue(resource, mutation.Path, mutation.Value);
                break;
            case "remove":
                RemoveValue(resource, mutation.Path);
                break;
            case "add":
                AddValue(resource, mutation.Path, mutation.Value);
                break;
        }
    }

    private static void SetValue(object obj, string path, object? value)
    {
        var parts = path.Split('.');
        object? current = obj;

        for (int i = 0; i < parts.Length - 1; i++)
        {
            current = DotPathResolver.Resolve(current, parts[i]);
            if (current == null)
                return;
        }

        var propertyName = parts[^1];
        if (current is Dictionary<string, object?> dict)
        {
            dict[propertyName] = value;
        }
        else if (current != null)
        {
            var prop = current.GetType().GetProperty(propertyName, System.Reflection.BindingFlags.IgnoreCase | System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance);
            prop?.SetValue(current, value);
        }
    }

    private static void RemoveValue(object obj, string path)
    {
        var parts = path.Split('.');
        object? current = obj;

        for (int i = 0; i < parts.Length - 1; i++)
        {
            current = DotPathResolver.Resolve(current, parts[i]);
            if (current == null)
                return;
        }

        var propertyName = parts[^1];
        if (current is Dictionary<string, object?> dict)
        {
            dict.Remove(propertyName);
        }
        else if (current != null)
        {
            var prop = current.GetType().GetProperty(propertyName, System.Reflection.BindingFlags.IgnoreCase | System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance);
            if (prop != null && prop.CanWrite)
            {
                prop.SetValue(current, null);
            }
        }
    }

    private static void AddValue(object obj, string path, object? value)
    {
        // For arrays/lists - would need to handle collection types
        SetValue(obj, path, value);
    }

    private static object? ResolveValue(object obj, string path)
    {
        return DotPathResolver.Resolve(obj, path);
    }

    private static string GetParentPath(string path)
    {
        var lastDot = path.LastIndexOf('.');
        return lastDot > 0 ? path.Substring(0, lastDot) : string.Empty;
    }

    private static string GetPropertyName(string path)
    {
        var lastDot = path.LastIndexOf('.');
        return lastDot >= 0 ? path.Substring(lastDot + 1) : path;
    }
}
