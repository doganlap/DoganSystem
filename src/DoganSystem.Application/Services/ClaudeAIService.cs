using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Anthropic.SDK;
using Anthropic.SDK.Messaging;

namespace DoganSystem.Application.Services
{
    /// <summary>
    /// Service for interacting with Claude AI via Anthropic SDK
    /// </summary>
    public class ClaudeAIService : IClaudeAIService
    {
        private readonly AnthropicClient? _client;
        private readonly ILogger<ClaudeAIService> _logger;
        private readonly string _defaultModel = "claude-sonnet-4-20250514";
        private readonly bool _isConfigured;

        public ClaudeAIService(IConfiguration configuration, ILogger<ClaudeAIService> logger)
        {
            _logger = logger;

            var apiKey = configuration["Anthropic:ApiKey"]
                ?? Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");

            if (string.IsNullOrEmpty(apiKey))
            {
                _logger.LogWarning("Anthropic API key not configured. Claude AI features disabled.");
                _isConfigured = false;
                _client = null;
            }
            else
            {
                _client = new AnthropicClient(apiKey);
                _isConfigured = true;
                _logger.LogInformation("Claude AI Service initialized successfully");
            }
        }

        public bool IsConfigured => _isConfigured;

        /// <summary>
        /// Send a chat message to Claude
        /// </summary>
        public async Task<ClaudeResponse> ChatAsync(
            string message,
            string? systemPrompt = null,
            string? model = null,
            int maxTokens = 4096,
            float temperature = 0.7f)
        {
            if (!_isConfigured || _client == null)
            {
                return new ClaudeResponse
                {
                    Success = false,
                    Error = "Claude AI not configured. Set Anthropic:ApiKey in configuration."
                };
            }

            try
            {
                var messageParams = new MessageParameters
                {
                    Model = model ?? _defaultModel,
                    MaxTokens = maxTokens,
                    Temperature = (decimal)temperature,
                    System = new List<SystemMessage>
                    {
                        new SystemMessage(systemPrompt ?? "You are a helpful AI assistant for DoganSystem.")
                    },
                    Messages = new List<Message>
                    {
                        new Message(RoleType.User, message)
                    }
                };

                var response = await _client.Messages.GetClaudeMessageAsync(messageParams);

                return new ClaudeResponse
                {
                    Success = true,
                    Content = response.Message.ToString(),
                    Model = response.Model,
                    InputTokens = response.Usage.InputTokens,
                    OutputTokens = response.Usage.OutputTokens,
                    Timestamp = DateTime.UtcNow
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Claude API error");
                return new ClaudeResponse
                {
                    Success = false,
                    Error = ex.Message
                };
            }
        }

        /// <summary>
        /// Analyze data using Claude
        /// </summary>
        public async Task<ClaudeResponse> AnalyzeDataAsync(
            object data,
            string analysisType = "general",
            string? customPrompt = null)
        {
            var prompts = new Dictionary<string, string>
            {
                ["general"] = "Analyze the following data and provide insights:",
                ["sales"] = "Analyze this sales data and identify trends, opportunities, and recommendations:",
                ["inventory"] = "Analyze this inventory data and identify stock issues and optimization opportunities:",
                ["hr"] = "Analyze this HR data and provide insights on workforce and performance:",
                ["financial"] = "Analyze this financial data and provide insights on cash flow and profitability:",
                ["crm"] = "Analyze this CRM data and identify customer trends and engagement strategies:"
            };

            var systemPrompt = @"You are a business analyst AI for DoganSystem.
Analyze data and provide actionable insights in JSON format with the following structure:
{
    ""summary"": ""Brief overview"",
    ""key_findings"": [""finding1"", ""finding2""],
    ""recommendations"": [""rec1"", ""rec2""],
    ""risks"": [""risk1"", ""risk2""],
    ""metrics"": {""metric1"": value}
}";

            var userPrompt = customPrompt ?? prompts.GetValueOrDefault(analysisType, prompts["general"]);
            userPrompt += $"\n\nData:\n```json\n{JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true })}\n```";

            return await ChatAsync(
                message: userPrompt,
                systemPrompt: systemPrompt,
                temperature: 0.3f
            );
        }

        /// <summary>
        /// Generate a task description for a workflow
        /// </summary>
        public async Task<ClaudeResponse> GenerateWorkflowTaskAsync(
            string workflowName,
            object? context = null)
        {
            var systemPrompt = @"You are an AI workflow manager for DoganSystem.
Generate detailed task instructions for AI employees to execute.
Include step-by-step actions, expected outcomes, and validation criteria.";

            var prompt = $"Generate a detailed task for the workflow: {workflowName}";
            if (context != null)
            {
                prompt += $"\n\nContext:\n```json\n{JsonSerializer.Serialize(context, new JsonSerializerOptions { WriteIndented = true })}\n```";
            }

            return await ChatAsync(
                message: prompt,
                systemPrompt: systemPrompt,
                temperature: 0.5f
            );
        }

        /// <summary>
        /// Process an ERPNext action with AI assistance
        /// </summary>
        public async Task<ClaudeResponse> ProcessErpNextActionAsync(
            string actionType,
            string doctype,
            object? data = null)
        {
            var systemPrompt = $@"You are an ERPNext automation AI for DoganSystem.
Help with {actionType} operations on {doctype} documents.
Provide structured responses that can be directly used in ERPNext.";

            var prompt = $"Help with {actionType} for {doctype}.";
            if (data != null)
            {
                prompt += $"\n\nData:\n```json\n{JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true })}\n```";
            }

            return await ChatAsync(
                message: prompt,
                systemPrompt: systemPrompt,
                temperature: 0.3f
            );
        }
    }

    /// <summary>
    /// Response from Claude AI
    /// </summary>
    public class ClaudeResponse
    {
        public bool Success { get; set; }
        public string? Content { get; set; }
        public string? Error { get; set; }
        public string? Model { get; set; }
        public int InputTokens { get; set; }
        public int OutputTokens { get; set; }
        public DateTime Timestamp { get; set; }
    }

    /// <summary>
    /// Interface for Claude AI Service
    /// </summary>
    public interface IClaudeAIService
    {
        bool IsConfigured { get; }
        Task<ClaudeResponse> ChatAsync(string message, string? systemPrompt = null, string? model = null, int maxTokens = 4096, float temperature = 0.7f);
        Task<ClaudeResponse> AnalyzeDataAsync(object data, string analysisType = "general", string? customPrompt = null);
        Task<ClaudeResponse> GenerateWorkflowTaskAsync(string workflowName, object? context = null);
        Task<ClaudeResponse> ProcessErpNextActionAsync(string actionType, string doctype, object? data = null);
    }
}
