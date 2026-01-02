using AutoMapper;
using DoganSystem.Modules.TenantManagement.Domain;
using DoganSystem.Modules.TenantManagement.Application.Dtos;
using DoganSystem.Modules.ErpNext.Domain;
using DoganSystem.Modules.ErpNext.Application.Dtos;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using DoganSystem.Modules.AgentOrchestrator.Application.Dtos;
using DoganSystem.Modules.Subscription.Domain;
using DoganSystem.Modules.Subscription.Application.Dtos;

namespace DoganSystem.Application.ObjectMapper
{
    public class DoganSystemApplicationAutoMapperProfile : Profile
    {
        public DoganSystemApplicationAutoMapperProfile()
        {
            // Tenant Management
            CreateMap<Tenant, TenantDto>();
            CreateMap<CreateTenantDto, Tenant>();
            CreateMap<UpdateTenantDto, Tenant>();

            // ERPNext
            CreateMap<ErpNextInstance, ErpNextInstanceDto>();
            CreateMap<CreateErpNextInstanceDto, ErpNextInstance>();
            CreateMap<UpdateErpNextInstanceDto, ErpNextInstance>();

            // Employee Agent
            CreateMap<EmployeeAgent, EmployeeAgentDto>();
            CreateMap<CreateEmployeeAgentDto, EmployeeAgent>();
            CreateMap<UpdateEmployeeAgentDto, EmployeeAgent>();

            // Subscription
            CreateMap<Subscription, SubscriptionDto>();
            CreateMap<CreateSubscriptionDto, Subscription>();
            CreateMap<UpdateSubscriptionDto, Subscription>();
        }
    }
}
