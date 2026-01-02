using System.Text.Json;

namespace DoganSystem.Application.Policy;

public class DotPathResolver
{
    public static object? Resolve(object obj, string path)
    {
        if (string.IsNullOrEmpty(path))
            return null;

        var parts = path.Split('.');
        object? current = obj;

        foreach (var part in parts)
        {
            if (current == null)
                return null;

            // Handle dictionary access (e.g., metadata.labels.dataClassification)
            if (current is Dictionary<string, object?> dict)
            {
                if (!dict.TryGetValue(part, out current))
                    return null;
            }
            // Handle JSON element
            else if (current is JsonElement jsonElement)
            {
                if (jsonElement.ValueKind == JsonValueKind.Object && jsonElement.TryGetProperty(part, out var prop))
                {
                    current = prop;
                }
                else
                {
                    return null;
                }
            }
            // Handle object property via reflection
            else
            {
                var type = current.GetType();
                var prop = type.GetProperty(part, System.Reflection.BindingFlags.IgnoreCase | System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Instance);
                if (prop == null)
                    return null;

                current = prop.GetValue(current);
            }
        }

        // Convert JsonElement to actual value
        if (current is JsonElement element)
        {
            return element.ValueKind switch
            {
                JsonValueKind.String => element.GetString(),
                JsonValueKind.Number => element.GetInt32(),
                JsonValueKind.True => true,
                JsonValueKind.False => false,
                JsonValueKind.Null => null,
                _ => element.ToString()
            };
        }

        return current;
    }
}
