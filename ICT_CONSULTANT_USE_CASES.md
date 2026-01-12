# 🏢 ICT Consultant Office - Use Cases & Scenarios

## Overview

This document describes how an **ICT Consultant Office** can use DoganSystem to manage their business operations, employees, and customer relationships.

---

## 👥 10 Scenarios: Employee Interactions

### Scenario 1: Onboard New Employee Agent
**Use Case:** Hire a new consultant and set them up as an AI agent

**Steps:**
1. **Create Employee Agent** via `/api/agents`
   ```json
   {
     "tenantId": "office-tenant-id",
     "employeeName": "Ahmed Al-Saud",
     "role": "Senior IT Consultant",
     "department": "Infrastructure",
     "capabilities": ["network-design", "cloud-migration", "security-audit"],
     "status": "Available"
   }
   ```
2. System automatically syncs to Python orchestrator
3. Agent becomes available for customer projects

**Benefits:**
- ✅ Instant agent availability
- ✅ Automatic capability tracking
- ✅ Team integration

---

### Scenario 2: Assign Employee to Customer Project
**Use Case:** Assign consultant to work on a customer's ERPNext system

**Steps:**
1. **Link Employee Agent to Tenant** (customer)
   - Update agent's `TenantId` or create project assignment
2. **Create ERPNext Instance** for customer
   ```json
   {
     "name": "Customer ABC ERPNext",
     "baseUrl": "https://customer-abc.erpnext.com",
     "tenantId": "customer-abc-id",
     "apiKey": "customer-api-key",
     "apiSecret": "customer-api-secret"
   }
   ```
3. Agent can now access customer's ERPNext system

**Benefits:**
- ✅ Clear project assignment
- ✅ Secure access management
- ✅ Customer isolation

---

### Scenario 3: Track Employee Availability
**Use Case:** Check which consultants are available for new projects

**Steps:**
1. **Query Agents by Status**
   ```
   GET /api/agents?status=Available
   ```
2. View available consultants
3. Assign to new customer project

**Benefits:**
- ✅ Real-time availability
- ✅ Resource optimization
- ✅ Quick project assignment

---

### Scenario 4: Employee Task Delegation
**Use Case:** Senior consultant delegates task to junior consultant

**Steps:**
1. **Set Manager-Worker Relationship**
   ```json
   {
     "managerId": "senior-consultant-id",
     "teamId": "infrastructure-team-id"
   }
   ```
2. Senior consultant assigns task via agent system
3. Junior consultant receives task in Python orchestrator

**Benefits:**
- ✅ Clear hierarchy
- ✅ Task distribution
- ✅ Team collaboration

---

### Scenario 5: Employee Performance Tracking
**Use Case:** Track consultant's work on customer projects

**Steps:**
1. **Query Agent Activities**
   - View agent's assigned customers
   - Track ERPNext instances managed
   - Monitor task completion
2. **Generate Reports** via Reports module
3. Review performance metrics

**Benefits:**
- ✅ Performance visibility
- ✅ Resource utilization
- ✅ Billing accuracy

---

### Scenario 6: Employee Capability Management
**Use Case:** Update consultant's skills and capabilities

**Steps:**
1. **Update Agent Capabilities**
   ```json
   {
     "capabilities": [
       "network-design",
       "cloud-migration",
       "security-audit",
       "database-optimization"  // New skill added
     ]
   }
   ```
2. System updates agent profile
3. Agent becomes available for new project types

**Benefits:**
- ✅ Skill tracking
- ✅ Project matching
- ✅ Career development

---

### Scenario 7: Employee Team Management
**Use Case:** Organize consultants into project teams

**Steps:**
1. **Create Team Structure**
   - Assign agents to teams
   - Set team leaders
   - Define team capabilities
2. **Assign Team to Customer Project**
3. Team works collaboratively on customer system

**Benefits:**
- ✅ Team organization
- ✅ Collaborative work
- ✅ Project management

---

### Scenario 8: Employee Status Updates
**Use Case:** Consultant updates their status (Available, Busy, Away)

**Steps:**
1. **Update Agent Status**
   ```
   PUT /api/agents/{id}
   {
     "status": "Busy"  // Working on customer project
   }
   ```
2. System reflects status change
3. Other employees see updated availability

**Benefits:**
- ✅ Real-time status
- ✅ Workload visibility
- ✅ Resource planning

---

### Scenario 9: Employee Access to Customer Systems
**Use Case:** Consultant needs to access customer's ERPNext for support

**Steps:**
1. **Query ERPNext Instances**
   ```
   GET /api/erpnext?tenantId={customer-id}
   ```
2. **Test Connection** to verify access
   ```
   POST /api/erpnext/{id}/test-connection
   ```
3. Consultant accesses customer system via ERPNext API

**Benefits:**
- ✅ Secure access
- ✅ Connection verification
- ✅ Customer support

---

### Scenario 10: Employee Knowledge Sharing
**Use Case:** Consultant documents solution for team knowledge base

**Steps:**
1. **Create Evidence/Assessment** in GRC system
   - Document solution approach
   - Attach configuration files
   - Link to customer project
2. **Share with Team** via Workflow module
3. Team members can access knowledge base

**Benefits:**
- ✅ Knowledge management
- ✅ Team learning
- ✅ Solution reuse

---

## 🏢 10 Scenarios: Customer Interactions

### Scenario 1: Onboard New Customer
**Use Case:** New customer signs up for ICT consulting services

**Steps:**
1. **Create Tenant** for customer
   ```json
   {
     "name": "ABC Manufacturing Company",
     "subdomain": "abc-manufacturing",
     "subscriptionTier": "Professional",
     "trialDays": 30,
     "status": "Trial"
   }
   ```
2. **Create Subscription**
   ```json
   {
     "tenantId": "customer-id",
     "planType": "Professional",
     "startDate": "2025-01-22",
     "status": "Active"
   }
   ```
3. Customer gets access to system

**Benefits:**
- ✅ Quick onboarding
- ✅ Trial period management
- ✅ Subscription tracking

---

### Scenario 2: Setup Customer ERPNext System
**Use Case:** Configure ERPNext instance for customer's business

**Steps:**
1. **Create ERPNext Instance**
   ```json
   {
     "name": "ABC Manufacturing ERPNext",
     "baseUrl": "https://abc.erpnext.com",
     "tenantId": "customer-id",
     "apiKey": "customer-api-key",
     "apiSecret": "customer-api-secret",
     "siteName": "abc-manufacturing",
     "isActive": true
   }
   ```
2. **Test Connection** to verify setup
3. **Assign Employee Agent** to manage customer system

**Benefits:**
- ✅ System integration
- ✅ Connection verification
- ✅ Support assignment

---

### Scenario 3: Customer Support Request
**Use Case:** Customer needs help with their ERPNext system

**Steps:**
1. **Customer submits ticket** (via email or system)
2. **Assign Available Agent**
   ```
   GET /api/agents?status=Available
   ```
3. **Agent accesses customer ERPNext**
   ```
   GET /api/erpnext?tenantId={customer-id}
   ```
4. **Agent resolves issue** and documents solution

**Benefits:**
- ✅ Quick response
- ✅ Expert assignment
- ✅ Issue resolution

---

### Scenario 4: Customer System Migration
**Use Case:** Migrate customer from old system to ERPNext

**Steps:**
1. **Create Migration Project**
   - Link customer tenant
   - Assign migration team
   - Set timeline
2. **Configure ERPNext Instance** for customer
3. **Use Agents** to perform data migration
4. **Track Progress** via Action Plans module
5. **Document Process** via Evidence module

**Benefits:**
- ✅ Project management
- ✅ Team coordination
- ✅ Process documentation

---

### Scenario 5: Customer Compliance Assessment
**Use Case:** Perform GRC compliance assessment for customer

**Steps:**
1. **Create Assessment** in GRC system
   ```json
   {
     "customerId": "customer-tenant-id",
     "assessmentType": "Compliance",
     "framework": "ISO 27001"
   }
   ```
2. **Assign Auditor Agent** to assessment
3. **Collect Evidence** from customer systems
4. **Generate Report** via Reports module
5. **Share with Customer** via Notifications

**Benefits:**
- ✅ Compliance verification
- ✅ Risk identification
- ✅ Customer confidence

---

### Scenario 6: Customer Subscription Management
**Use Case:** Customer wants to upgrade subscription plan

**Steps:**
1. **View Current Subscription**
   ```
   GET /api/subscriptions?tenantId={customer-id}
   ```
2. **Update Subscription Plan**
   ```json
   {
     "planType": "Enterprise",  // Upgrade from Professional
     "monthlyPrice": 999.00
   }
   ```
3. **Update Billing Date**
4. **Notify Customer** of upgrade

**Benefits:**
- ✅ Flexible plans
- ✅ Easy upgrades
- ✅ Billing management

---

### Scenario 7: Customer System Monitoring
**Use Case:** Monitor customer's ERPNext system health

**Steps:**
1. **Test ERPNext Connection** regularly
   ```
   POST /api/erpnext/{id}/test-connection
   ```
2. **Check System Status** via Python orchestrator
3. **Generate Alerts** if issues detected
4. **Assign Support Agent** if needed

**Benefits:**
- ✅ Proactive monitoring
- ✅ Issue prevention
- ✅ Customer satisfaction

---

### Scenario 8: Customer Training Session
**Use Case:** Train customer employees on ERPNext usage

**Steps:**
1. **Schedule Training** via Compliance Calendar
2. **Assign Training Agent** (consultant)
3. **Create Training Materials** in Evidence module
4. **Track Attendance** via Assessments
5. **Follow-up** via Notifications

**Benefits:**
- ✅ Customer education
- ✅ System adoption
- ✅ Relationship building

---

### Scenario 9: Customer Custom Development
**Use Case:** Develop custom features for customer's ERPNext

**Steps:**
1. **Create Development Project**
   - Link to customer tenant
   - Assign development team
   - Set requirements
2. **Track Development** via Action Plans
3. **Test in Customer System** via ERPNext API
4. **Deploy and Document** via Evidence module

**Benefits:**
- ✅ Custom solutions
- ✅ Project tracking
- ✅ Quality assurance

---

### Scenario 10: Customer Billing & Invoicing
**Use Case:** Generate invoice for customer services

**Steps:**
1. **Track Service Usage**
   - Agent hours worked
   - Projects completed
   - System maintenance
2. **Generate Invoice** via ERPNext (customer's system)
3. **Update Subscription** billing
4. **Send Invoice** to customer
5. **Track Payment** via Subscription module

**Benefits:**
- ✅ Accurate billing
- ✅ Payment tracking
- ✅ Financial management

---

## 🔄 Complete Workflow Examples

### Workflow 1: New Customer Onboarding

```
1. Sales Team
   └─► Creates Tenant (customer)
       └─► Creates Subscription (Professional plan)
           └─► Sets Trial Period (30 days)

2. Technical Team
   └─► Creates ERPNext Instance
       └─► Tests Connection
           └─► Configures System

3. Support Team
   └─► Assigns Employee Agent
       └─► Creates Initial Assessment
           └─► Schedules Training

4. Customer
   └─► Receives Access
       └─► Starts Using System
           └─► Gets Support from Agent
```

---

### Workflow 2: Customer Support Request

```
1. Customer
   └─► Submits Support Request
       └─► System Creates Ticket

2. System
   └─► Finds Available Agent
       └─► Assigns to Ticket
           └─► Notifies Agent

3. Agent
   └─► Accesses Customer ERPNext
       └─► Diagnoses Issue
           └─► Resolves Problem
               └─► Documents Solution

4. Customer
   └─► Receives Resolution
       └─► Confirms Fix
           └─► Ticket Closed
```

---

### Workflow 3: Employee Project Assignment

```
1. Project Manager
   └─► Creates Project
       └─► Links Customer Tenant
           └─► Defines Requirements

2. System
   └─► Finds Available Agents
       └─► Matches Capabilities
           └─► Suggests Team

3. Project Manager
   └─► Assigns Agents
       └─► Sets Timeline
           └─► Creates Action Plan

4. Agents
   └─► Access Customer System
       └─► Work on Project
           └─► Update Progress
               └─► Complete Tasks
```

---

## 📊 Business Benefits Summary

### For ICT Consultant Office:

1. **Multi-Tenant Management**
   - ✅ Manage multiple customers in one system
   - ✅ Isolated customer data
   - ✅ Scalable architecture

2. **Employee Management**
   - ✅ Track consultant availability
   - ✅ Assign to projects
   - ✅ Monitor performance

3. **Customer Management**
   - ✅ Complete customer lifecycle
   - ✅ Subscription management
   - ✅ Support tracking

4. **Integration**
   - ✅ ERPNext for customer systems
   - ✅ AI Agents for automation
   - ✅ GRC for compliance

5. **Automation**
   - ✅ Agent-based workflows
   - ✅ Automated notifications
   - ✅ Self-service capabilities

---

## 🎯 Key Features Used

### Tenant Management Module:
- Create/Manage customer tenants
- Trial period management
- Tenant activation/suspension

### ERPNext Module:
- Customer ERPNext instance management
- Connection testing
- API integration

### Agent Orchestrator Module:
- Employee agent management
- Team organization
- Task assignment

### Subscription Module:
- Customer subscription plans
- Billing management
- Renewal tracking

### GRC System:
- Compliance assessments
- Evidence management
- Risk tracking
- Reports generation

---

## 💡 Best Practices

### For Employee Management:
1. ✅ Keep agent status updated
2. ✅ Document capabilities accurately
3. ✅ Use teams for project organization
4. ✅ Track performance metrics

### For Customer Management:
1. ✅ Complete onboarding process
2. ✅ Test ERPNext connections regularly
3. ✅ Monitor subscription status
4. ✅ Provide proactive support

### For Project Management:
1. ✅ Use Action Plans for tracking
2. ✅ Document solutions in Evidence
3. ✅ Generate reports regularly
4. ✅ Communicate via Notifications

---

## 📈 Success Metrics

### Employee Metrics:
- Agent utilization rate
- Project completion rate
- Customer satisfaction (per agent)
- Response time

### Customer Metrics:
- Customer retention rate
- Subscription renewal rate
- Support ticket resolution time
- System uptime

### Business Metrics:
- Revenue per customer
- Average project duration
- Employee productivity
- Customer acquisition cost

---

**Last Updated:** 2025-01-22
