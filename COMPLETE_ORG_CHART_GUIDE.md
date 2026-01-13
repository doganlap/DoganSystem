# Complete ERPNext Organizational Chart - Guide

## Overview

This system creates a **complete virtual AI organization** to manage your ERPNext installation, with specialized employees for every module and automated workflows for all business processes.

## What You Get

### 📊 Complete Organization

**80+ AI Employees** across 12 departments:

#### Executive Team (4 employees)
- **CEO** - عبدالله المهندس (Abdullah Al-Muhandis) - Strategic oversight
- **CTO** - نورة التقنية (Noura Al-Tiqniya) - Technology strategy
- **CFO** - خالد المالي (Khaled Al-Mali) - Financial oversight
- **COO** - ريم العمليات (Reem Al-Amaliyat) - Operations management

#### CRM Department (8 employees)
- 1 Director
- 2 Team Leads (Lead Management, Customer Management)
- 4 Specialists (Lead & Customer processing)
- 1 Analyst

#### Sales Department (14 employees)
- 1 Director
- 3 Team Leads (Quotations, Orders, Invoices)
- 9 Specialists
- 1 Analyst

#### Procurement Department (7 employees)
- 1 Director
- 2 Team Leads (Suppliers, Purchase Orders)
- 3 Specialists
- 1 Analyst

#### Inventory Department (9 employees)
- 1 Director
- 3 Team Leads (Warehouse, Items, Stock Control)
- 4 Warehouse Specialists
- 1 Analyst

#### Finance/Accounting Department (9 employees)
- 1 Director
- 3 Team Leads (AR, AP, GL)
- 4 Accountants
- 1 Financial Analyst

#### HR Department (7 employees)
- 1 Director
- 3 Team Leads (Recruitment, Payroll, Attendance)
- 3 HR Specialists

#### Project Management Office (5 employees)
- 1 PMO Director
- 3 Project Managers
- 1 Timesheet Coordinator

#### Manufacturing Department (4 employees)
- 1 Director
- 1 Production Planner
- 1 Work Order Lead
- 1 BOM Engineer

#### Support Department (7 employees)
- 1 Director
- 1 Team Lead
- 5 Support Specialists

#### Quality Department (5 employees)
- 1 Director
- 1 QC Lead
- 3 Quality Inspectors

#### Assets Department (3 employees)
- 1 Director
- 1 Maintenance Lead
- 1 Asset Custodian

#### IT Department (4 employees)
- 1 Director
- 1 System Administrator
- 1 Customization Developer
- 1 Data Analyst

### 🔄 40+ Automated Workflows

Complete workflow automation for:

- **CRM**: Lead processing, customer data cleanup, pipeline analysis
- **Sales**: Quotation follow-up, order processing, invoice generation, performance analysis
- **Procurement**: Reorder automation, PO follow-up, spend analysis
- **Inventory**: Stock checks, reconciliation, movement analysis
- **Accounting**: Payment matching, AR aging, month-end close, financial analysis
- **HR**: Attendance processing, payroll, leave approval
- **Projects**: Task updates, project reviews
- **Manufacturing**: Production planning, work order completion
- **Support**: Ticket assignment, SLA monitoring
- **Quality**: Inspection scheduling, defect analysis
- **IT**: System health checks, customization review, data analysis

## Quick Setup (5 Minutes)

### Step 1: Prerequisites

Ensure you have:
```bash
# Required environment variables in .env
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_key
ERPNEXT_API_SECRET=your_secret
CLAUDE_API_KEY=your_claude_key
```

### Step 2: Run Setup

```bash
cd agent-setup
python create_complete_organization.py
```

This will:
- ✅ Create 80+ AI employees
- ✅ Build organizational hierarchy
- ✅ Register 40+ workflows
- ✅ Generate visualizations
- ✅ Create documentation files

### Step 3: View Your Organization

Open the generated files:
```bash
# View in browser
start org_chart.html          # Windows
open org_chart.html           # Mac
xdg-open org_chart.html       # Linux

# View text format
cat org_chart_visualization.txt

# View JSON data
cat erpnext_complete_org_chart.json
```

## Organizational Structure

### Hierarchy

```
CEO (عبدالله المهندس)
├── CTO (نورة التقنية)
│   └── IT Director (علي التقنية)
│       ├── System Administrator
│       ├── Customization Developer
│       └── Data Analyst
│
├── CFO (خالد المالي)
│   ├── Finance Director (سعد المحاسبة)
│   │   ├── AR Lead → Accountants
│   │   ├── AP Lead → Accountants
│   │   ├── GL Lead → Accountants
│   │   └── Financial Analyst
│   │
│   └── Assets Director (فيصل الأصول)
│       ├── Maintenance Lead
│       └── Asset Custodian
│
└── COO (ريم العمليات)
    ├── CRM Director → Leads → Specialists
    ├── Sales Director → Leads → Specialists
    ├── Procurement Director → Leads → Specialists
    ├── Inventory Director → Leads → Specialists
    ├── PMO Director → Project Managers
    ├── Manufacturing Director → Planners → Engineers
    ├── Support Director → Lead → Specialists
    └── Quality Director → QC Lead → Inspectors
```

### Employee Types

#### Explore Agents (Analysts)
- **Role**: System analysis, data exploration, insights
- **Examples**: CRM Analyst, Sales Analyst, Financial Analyst
- **Tasks**: Analyze configurations, generate reports, identify trends

#### Plan Agents (Architects/Directors)
- **Role**: Strategic planning, process design
- **Examples**: CEO, Directors, Production Planner
- **Tasks**: Design processes, create strategies, plan implementations

#### Operations Agents (Specialists/Managers)
- **Role**: Execute workflows, process transactions
- **Examples**: Sales Specialists, Accountants, Support Agents
- **Tasks**: Process orders, manage data, execute workflows

## Using Your Organization

### Example 1: Assign Task to Specific Employee

```python
from claude_code_bridge import SubagentERPNextBridge

bridge = SubagentERPNextBridge(erpnext_base_url="http://localhost:8000")

# Get Sales Director
sales_director = bridge.employees.get("emp_sales_dir_001")

# Assign strategic task
task = bridge.assign_task(
    employee_id="emp_sales_dir_001",
    task_description="""
    Review last quarter's sales performance:
    1. Analyze sales trends by product category
    2. Compare actual vs targets
    3. Identify top-performing sales reps
    4. Create action plan for next quarter
    """
)

# Get prompt for Claude Code
prompt = bridge.get_task_prompt(task)
```

### Example 2: Execute Department Workflow

```python
from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator

orchestrator = EnhancedAutonomousOrchestrator(
    erpnext_base_url="http://localhost:8000"
)

# Execute Sales quotation follow-up workflow
result = orchestrator.execute_workflow("sales_quotation_followup")

print(f"Workflow executed by: {result['task_details']['employee_name']}")
print(f"Status: {result['task_details']['status']}")
```

### Example 3: Coordinate Multi-Department Process

```python
# Month-end closing involving multiple departments

# 1. Finance: Close accounting period
orchestrator.execute_workflow("acc_month_end")

# 2. Sales: Generate sales reports
orchestrator.execute_workflow("sales_month_end_closing")

# 3. Inventory: Stock reconciliation
orchestrator.execute_workflow("inv_reconciliation")

# 4. HR: Process payroll
orchestrator.execute_workflow("hr_payroll_processing")

# All departments working in coordination!
```

## Workflow Schedules

### Hourly Workflows
- Sales Order Processing
- Work Order Completion
- Support Ticket Assignment

### Daily Workflows
- Lead Processing (9 AM)
- Quotation Follow-up (10 AM)
- Invoice Generation (2 PM)
- Payment Matching (3 PM)
- Attendance Processing (5 PM)
- Stock Level Check (7 AM)
- System Health Check (6 AM)

### Weekly Workflows
- Customer Data Cleanup (Friday)
- Sales Performance Analysis (Monday)
- AR Aging Report (Thursday)
- Project Review (Friday)
- Process Optimization (Monday)

### Monthly Workflows
- Payroll Processing (25th)
- Month-End Close (Last day)
- Spend Analysis (5th)
- Inventory Analysis (1st)
- Financial Analysis (3rd)

## Customization

### Add Custom Employee

```python
# Create a specialized role
custom_employee = bridge.create_operations_employee(
    employee_name="متخصص مخصص",
    department="Custom",
    employee_id="emp_custom_001"
)

# Assign custom tasks
task = bridge.assign_task(
    employee_id="emp_custom_001",
    task_description="Your custom task here..."
)
```

### Add Custom Workflow

```python
orchestrator.create_custom_workflow(
    workflow_id="custom_workflow",
    name="Custom Business Process",
    description="Custom automation",
    task_description="""
    Your custom workflow steps:
    1. Step 1
    2. Step 2
    3. Step 3
    """,
    task_type="execute",
    schedule="daily_10am"
)
```

## Monitoring

### Check Organization Status

```python
# Get overall system status
status = bridge.get_system_status()

print(f"Total Employees: {status['employees']['total']}")
print(f"Available: {status['employees']['available']}")
print(f"Busy: {status['employees']['busy']}")

print(f"Total Tasks: {status['tasks']['total']}")
print(f"Completed: {status['tasks']['completed']}")
```

### View Department Performance

```python
# List employees by department
sales_team = bridge.list_employees(department="Sales")

print(f"Sales Department: {len(sales_team)} employees")
for emp in sales_team:
    print(f"  - {emp.employee_name} ({emp.role}): {emp.status}")
```

### Check Workflow Execution

```python
# Get workflow history
workflows = orchestrator.autonomous_workflows

for wf_id, wf in workflows.items():
    if wf['enabled']:
        print(f"{wf['name']}")
        print(f"  Last run: {wf['last_run']}")
        print(f"  Executions: {wf['execution_count']}")
```

## Files Generated

After running `create_complete_organization.py`:

| File | Description |
|------|-------------|
| `erpnext_complete_org_chart.json` | Complete org chart data (JSON) |
| `complete_org_employees.json` | All employee records with state |
| `workflow_summary.json` | Summary of all workflows |
| `org_chart_visualization.txt` | Text-based org chart |
| `org_chart.html` | Interactive HTML visualization |

## Best Practices

### 1. Department Coordination
- Use department workflows for routine tasks
- Assign cross-department projects to directors
- Let analysts provide insights to guide operations

### 2. Task Assignment
- Assign exploration tasks to Analysts (Explore agents)
- Assign planning tasks to Directors (Plan agents)
- Assign execution tasks to Specialists (Operations agents)

### 3. Workflow Management
- Start with default workflows
- Monitor execution results
- Customize based on your business needs
- Add new workflows as needed

### 4. Scaling
- Create additional specialists as workload grows
- Add team leads for larger departments
- Customize employee capabilities per role

## Troubleshooting

### Issue: Too many employees

**Solution**: Filter by department or role
```python
# Get only executives
execs = [e for e in bridge.employees.values()
         if "Director" in e.role or "CEO" in e.role]
```

### Issue: Workflow not executing

**Solution**: Check workflow status
```python
workflow = orchestrator.autonomous_workflows["workflow_id"]
print(f"Enabled: {workflow['enabled']}")
print(f"Last run: {workflow['last_run']}")
```

### Issue: Employee always busy

**Solution**: Check task status
```python
tasks = bridge.get_task_history(employee_id="emp_id")
pending = [t for t in tasks if t.status == "in_progress"]
print(f"Pending tasks: {len(pending)}")
```

## Integration with Existing System

This complete organization integrates seamlessly with:

- ✅ Your existing employee agent system
- ✅ Multi-tenant architecture
- ✅ Autonomous orchestrator
- ✅ ERPNext API
- ✅ Email integration
- ✅ All existing workflows

## Support

- **Full Org Chart**: Open `org_chart.html` in browser
- **Employee Data**: Check `erpnext_complete_org_chart.json`
- **Workflow Summary**: Review `workflow_summary.json`
- **Documentation**: See all `*.md` files in project root

---

**Your ERPNext is now managed by a complete AI organization with 80+ employees!** 🎉
