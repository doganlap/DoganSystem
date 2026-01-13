using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using DoganSystem.Modules.ConsultantOffers.Application.Dtos;
using DoganSystem.Modules.ConsultantOffers.Domain;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using DoganSystem.Modules.ErpNext.Domain;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Http;
using Volo.Abp;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;
using Volo.Abp.MultiTenancy;

namespace DoganSystem.Modules.ConsultantOffers.Application
{
    [Authorize]
    public class ConsultantOfferAppService : ApplicationService, IConsultantOfferAppService
    {
        private readonly IRepository<ConsultantOffer, Guid> _offerRepository;
        private readonly IRepository<EmployeeAgent, Guid> _employeeRepository;
        private readonly IRepository<ErpNextInstance, Guid> _erpNextRepository;
        private readonly ICurrentTenant _currentTenant;
        private readonly ILogger<ConsultantOfferAppService> _logger;
        private readonly HttpClient _httpClient;

        public ConsultantOfferAppService(
            IRepository<ConsultantOffer, Guid> offerRepository,
            IRepository<EmployeeAgent, Guid> employeeRepository,
            IRepository<ErpNextInstance, Guid> erpNextRepository,
            ICurrentTenant currentTenant,
            ILogger<ConsultantOfferAppService> logger,
            IHttpClientFactory httpClientFactory)
        {
            _offerRepository = offerRepository;
            _employeeRepository = employeeRepository;
            _erpNextRepository = erpNextRepository;
            _currentTenant = currentTenant;
            _logger = logger;
            _httpClient = httpClientFactory.CreateClient();
        }

        public async Task<ConsultantOfferDto> CreateAsync(CreateConsultantOfferDto input)
        {
            _logger.LogInformation("Creating consultant offer for employee: {EmployeeId}", input.EmployeeAgentId);

            // Verify employee exists
            var employee = await _employeeRepository.GetAsync(input.EmployeeAgentId);

            // Generate offer number
            var offerNumber = await GenerateOfferNumberAsync();

            var offer = new ConsultantOffer
            {
                TenantId = _currentTenant.Id ?? Guid.Empty,
                EmployeeAgentId = input.EmployeeAgentId,
                ErpNextInstanceId = input.ErpNextInstanceId,
                OfferNumber = offerNumber,
                Title = input.Title,
                Description = input.Description,
                OfferType = input.OfferType,
                Amount = input.Amount,
                Currency = input.Currency,
                StartDate = input.StartDate,
                EndDate = input.EndDate,
                Status = "Draft",
                ClientName = input.ClientName,
                ClientEmail = input.ClientEmail,
                ClientPhone = input.ClientPhone,
                TermsAndConditions = input.TermsAndConditions,
                Deliverables = input.Deliverables,
                PaymentTerms = input.PaymentTerms,
                Notes = input.Notes
            };

            // Create in ERPNext if requested
            if (input.CreateInErpNext && input.ErpNextInstanceId.HasValue)
            {
                try
                {
                    var erpNextInstance = await _erpNextRepository.GetAsync(input.ErpNextInstanceId.Value);
                    var quotationId = await CreateErpNextQuotationAsync(erpNextInstance, offer, employee);
                    offer.ErpNextQuotationId = quotationId;
                    _logger.LogInformation("Created ERPNext quotation: {QuotationId}", quotationId);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Failed to create ERPNext quotation");
                    // Continue without ERPNext integration
                }
            }

            offer = await _offerRepository.InsertAsync(offer);

            _logger.LogInformation("Consultant offer created: {OfferId}, Number: {OfferNumber}", offer.Id, offer.OfferNumber);

            return await MapToDtoAsync(offer);
        }

        public async Task<ConsultantOfferDto> UpdateAsync(Guid id, UpdateConsultantOfferDto input)
        {
            var offer = await _offerRepository.GetAsync(id);

            if (!string.IsNullOrEmpty(input.Title))
                offer.Title = input.Title;

            if (input.Description != null)
                offer.Description = input.Description;

            if (!string.IsNullOrEmpty(input.OfferType))
                offer.OfferType = input.OfferType;

            if (input.Amount.HasValue)
                offer.Amount = input.Amount.Value;

            if (!string.IsNullOrEmpty(input.Currency))
                offer.Currency = input.Currency;

            if (input.StartDate.HasValue)
                offer.StartDate = input.StartDate.Value;

            if (input.EndDate.HasValue)
                offer.EndDate = input.EndDate;

            if (!string.IsNullOrEmpty(input.Status))
                offer.Status = input.Status;

            if (input.ClientName != null)
                offer.ClientName = input.ClientName;

            if (input.ClientEmail != null)
                offer.ClientEmail = input.ClientEmail;

            if (input.ClientPhone != null)
                offer.ClientPhone = input.ClientPhone;

            if (input.TermsAndConditions != null)
                offer.TermsAndConditions = input.TermsAndConditions;

            if (input.Deliverables != null)
                offer.Deliverables = input.Deliverables;

            if (input.PaymentTerms != null)
                offer.PaymentTerms = input.PaymentTerms;

            if (input.Notes != null)
                offer.Notes = input.Notes;

            offer = await _offerRepository.UpdateAsync(offer);

            return await MapToDtoAsync(offer);
        }

        public async Task DeleteAsync(Guid id)
        {
            await _offerRepository.DeleteAsync(id);
        }

        public async Task<ConsultantOfferDto> GetAsync(Guid id)
        {
            var offer = await _offerRepository.GetAsync(id);
            return await MapToDtoAsync(offer);
        }

        public async Task<PagedResultDto<ConsultantOfferDto>> GetListAsync(ConsultantOfferListDto input)
        {
            var queryable = await _offerRepository.GetQueryableAsync();

            // Apply tenant filter
            if (_currentTenant.Id.HasValue)
            {
                queryable = queryable.Where(x => x.TenantId == _currentTenant.Id.Value);
            }

            // Apply filters
            if (input.EmployeeAgentId.HasValue)
            {
                queryable = queryable.Where(x => x.EmployeeAgentId == input.EmployeeAgentId.Value);
            }

            if (!string.IsNullOrEmpty(input.Status))
            {
                queryable = queryable.Where(x => x.Status == input.Status);
            }

            if (!string.IsNullOrEmpty(input.OfferType))
            {
                queryable = queryable.Where(x => x.OfferType == input.OfferType);
            }

            if (!string.IsNullOrEmpty(input.Filter))
            {
                queryable = queryable.Where(x =>
                    x.OfferNumber.Contains(input.Filter) ||
                    x.Title.Contains(input.Filter) ||
                    (x.ClientName != null && x.ClientName.Contains(input.Filter)));
            }

            // Apply sorting
            if (!string.IsNullOrEmpty(input.Sorting))
            {
                if (input.Sorting.StartsWith("-"))
                {
                    var propName = input.Sorting.Substring(1).Trim();
                    if (propName.Equals("CreationTime", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderByDescending(x => x.CreationTime);
                    else if (propName.Equals("Amount", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderByDescending(x => x.Amount);
                    else
                        queryable = queryable.OrderByDescending(x => x.CreationTime);
                }
                else
                {
                    var propName = input.Sorting.Trim();
                    if (propName.Equals("CreationTime", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderBy(x => x.CreationTime);
                    else if (propName.Equals("Amount", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderBy(x => x.Amount);
                    else
                        queryable = queryable.OrderBy(x => x.CreationTime);
                }
            }
            else
            {
                queryable = queryable.OrderByDescending(x => x.CreationTime);
            }

            var totalCount = queryable.Count();
            var items = queryable
                .Skip(input.SkipCount)
                .Take(input.MaxResultCount)
                .ToList();

            var dtos = new List<ConsultantOfferDto>();
            foreach (var offer in items)
            {
                dtos.Add(await MapToDtoAsync(offer));
            }

            return new PagedResultDto<ConsultantOfferDto>(totalCount, dtos);
        }

        public async Task<ConsultantOfferDto> SendAsync(Guid id)
        {
            var offer = await _offerRepository.GetAsync(id);

            if (offer.Status != "Draft")
            {
                throw new UserFriendlyException($"Offer {offer.OfferNumber} cannot be sent. Current status: {offer.Status}");
            }

            offer.Status = "Sent";
            offer.SentDate = DateTime.UtcNow;

            offer = await _offerRepository.UpdateAsync(offer);

            _logger.LogInformation("Offer sent: {OfferNumber}", offer.OfferNumber);

            return await MapToDtoAsync(offer);
        }

        public async Task<ConsultantOfferDto> AcceptAsync(Guid id)
        {
            var offer = await _offerRepository.GetAsync(id);

            if (offer.Status != "Sent")
            {
                throw new UserFriendlyException($"Offer {offer.OfferNumber} cannot be accepted. Current status: {offer.Status}");
            }

            offer.Status = "Accepted";
            offer.AcceptedDate = DateTime.UtcNow;

            // Create Sales Order in ERPNext if linked
            if (!string.IsNullOrEmpty(offer.ErpNextQuotationId) && offer.ErpNextInstanceId.HasValue)
            {
                try
                {
                    var erpNextInstance = await _erpNextRepository.GetAsync(offer.ErpNextInstanceId.Value);
                    var salesOrderId = await CreateErpNextSalesOrderAsync(erpNextInstance, offer);
                    offer.ErpNextSalesOrderId = salesOrderId;
                    _logger.LogInformation("Created ERPNext sales order: {SalesOrderId}", salesOrderId);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Failed to create ERPNext sales order");
                }
            }

            offer = await _offerRepository.UpdateAsync(offer);

            _logger.LogInformation("Offer accepted: {OfferNumber}", offer.OfferNumber);

            return await MapToDtoAsync(offer);
        }

        public async Task<ConsultantOfferDto> RejectAsync(Guid id, string? reason = null)
        {
            var offer = await _offerRepository.GetAsync(id);

            if (offer.Status != "Sent")
            {
                throw new UserFriendlyException($"Offer {offer.OfferNumber} cannot be rejected. Current status: {offer.Status}");
            }

            offer.Status = "Rejected";
            offer.RejectedDate = DateTime.UtcNow;
            offer.RejectionReason = reason;

            offer = await _offerRepository.UpdateAsync(offer);

            _logger.LogInformation("Offer rejected: {OfferNumber}, Reason: {Reason}", offer.OfferNumber, reason);

            return await MapToDtoAsync(offer);
        }

        private async Task<string> GenerateOfferNumberAsync()
        {
            var year = DateTime.UtcNow.Year;
            var queryable = await _offerRepository.GetQueryableAsync();
            var lastOffer = queryable
                .Where(x => x.OfferNumber.StartsWith($"OFF-{year}-"))
                .OrderByDescending(x => x.OfferNumber)
                .FirstOrDefault();

            int nextNumber = 1;
            if (lastOffer != null)
            {
                var parts = lastOffer.OfferNumber.Split('-');
                if (parts.Length >= 3 && int.TryParse(parts[2], out var lastNum))
                {
                    nextNumber = lastNum + 1;
                }
            }

            return $"OFF-{year}-{nextNumber:D4}";
        }

        private async Task<string> CreateErpNextQuotationAsync(ErpNextInstance instance, ConsultantOffer offer, EmployeeAgent employee)
        {
            var apiUrl = $"{instance.BaseUrl.TrimEnd('/')}/api/resource/Quotation";

            var quotationData = new
            {
                doctype = "Quotation",
                party_name = offer.ClientName ?? "Customer",
                quotation_to = "Customer",
                items = new[]
                {
                    new
                    {
                        item_code = $"CONSULTANT-{employee.EmployeeName}",
                        item_name = offer.Title,
                        description = offer.Description ?? offer.Title,
                        qty = 1,
                        rate = (double)offer.Amount,
                        uom = "Nos"
                    }
                },
                terms = offer.TermsAndConditions,
                valid_till = offer.EndDate?.ToString("yyyy-MM-dd") ?? DateTime.UtcNow.AddDays(30).ToString("yyyy-MM-dd"),
                custom_offer_number = offer.OfferNumber,
                custom_employee_agent_id = offer.EmployeeAgentId.ToString()
            };

            var json = JsonSerializer.Serialize(quotationData);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            if (!string.IsNullOrEmpty(instance.ApiKey) && !string.IsNullOrEmpty(instance.ApiSecret))
            {
                _httpClient.DefaultRequestHeaders.Clear();
                _httpClient.DefaultRequestHeaders.Add("Authorization", $"token {instance.ApiKey}:{instance.ApiSecret}");
            }

            var response = await _httpClient.PostAsync(apiUrl, content);
            response.EnsureSuccessStatusCode();

            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<JsonElement>(responseContent);

            if (result.TryGetProperty("data", out var data) && data.TryGetProperty("name", out var name))
            {
                return name.GetString() ?? string.Empty;
            }

            throw new UserFriendlyException("Failed to get quotation ID from ERPNext response");
        }

        private async Task<string> CreateErpNextSalesOrderAsync(ErpNextInstance instance, ConsultantOffer offer)
        {
            if (string.IsNullOrEmpty(offer.ErpNextQuotationId))
            {
                throw new UserFriendlyException("Cannot create sales order without quotation ID");
            }

            var apiUrl = $"{instance.BaseUrl.TrimEnd('/')}/api/method/frappe.client.make_sales_order";

            var requestData = new
            {
                quotation = offer.ErpNextQuotationId
            };

            var json = JsonSerializer.Serialize(requestData);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            if (!string.IsNullOrEmpty(instance.ApiKey) && !string.IsNullOrEmpty(instance.ApiSecret))
            {
                _httpClient.DefaultRequestHeaders.Clear();
                _httpClient.DefaultRequestHeaders.Add("Authorization", $"token {instance.ApiKey}:{instance.ApiSecret}");
            }

            var response = await _httpClient.PostAsync(apiUrl, content);
            response.EnsureSuccessStatusCode();

            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<JsonElement>(responseContent);

            if (result.TryGetProperty("message", out var message) && message.TryGetProperty("name", out var name))
            {
                return name.GetString() ?? string.Empty;
            }

            throw new UserFriendlyException("Failed to get sales order ID from ERPNext response");
        }

        private async Task<ConsultantOfferDto> MapToDtoAsync(ConsultantOffer offer)
        {
            var dto = new ConsultantOfferDto
            {
                Id = offer.Id,
                TenantId = offer.TenantId,
                EmployeeAgentId = offer.EmployeeAgentId,
                ErpNextInstanceId = offer.ErpNextInstanceId,
                OfferNumber = offer.OfferNumber,
                Title = offer.Title,
                Description = offer.Description,
                OfferType = offer.OfferType,
                Amount = offer.Amount,
                Currency = offer.Currency,
                StartDate = offer.StartDate,
                EndDate = offer.EndDate,
                Status = offer.Status,
                ClientName = offer.ClientName,
                ClientEmail = offer.ClientEmail,
                ClientPhone = offer.ClientPhone,
                ErpNextQuotationId = offer.ErpNextQuotationId,
                ErpNextSalesOrderId = offer.ErpNextSalesOrderId,
                ErpNextCustomerId = offer.ErpNextCustomerId,
                TermsAndConditions = offer.TermsAndConditions,
                Deliverables = offer.Deliverables,
                PaymentTerms = offer.PaymentTerms,
                SentDate = offer.SentDate,
                AcceptedDate = offer.AcceptedDate,
                RejectedDate = offer.RejectedDate,
                RejectionReason = offer.RejectionReason,
                Notes = offer.Notes,
                CreationTime = offer.CreationTime,
                LastModificationTime = offer.LastModificationTime
            };

            // Load employee name
            var employee = await _employeeRepository.FindAsync(offer.EmployeeAgentId);
            if (employee != null)
            {
                dto.EmployeeName = employee.EmployeeName;
            }

            // Load ERPNext instance name
            if (offer.ErpNextInstanceId.HasValue)
            {
                var erpNextInstance = await _erpNextRepository.FindAsync(offer.ErpNextInstanceId.Value);
                if (erpNextInstance != null)
                {
                    dto.ErpNextInstanceName = erpNextInstance.Name;
                }
            }

            return dto;
        }
    }

    public interface IConsultantOfferAppService : IApplicationService
    {
        Task<ConsultantOfferDto> CreateAsync(CreateConsultantOfferDto input);
        Task<ConsultantOfferDto> UpdateAsync(Guid id, UpdateConsultantOfferDto input);
        Task DeleteAsync(Guid id);
        Task<ConsultantOfferDto> GetAsync(Guid id);
        Task<PagedResultDto<ConsultantOfferDto>> GetListAsync(ConsultantOfferListDto input);
        Task<ConsultantOfferDto> SendAsync(Guid id);
        Task<ConsultantOfferDto> AcceptAsync(Guid id);
        Task<ConsultantOfferDto> RejectAsync(Guid id, string? reason = null);
    }
}
