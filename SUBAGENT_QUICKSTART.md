# Claude Code Subagent ERP Employees - Quick Start

## Overview

This system integrates **Claude Code's built-in subagents** with your ERPNext installation, allowing AI agents to work as virtual employees managing your ERP system.

## What You Get

- **3 Types of AI Employees**:
  - **System Analyst** (Explore agent) - Analyzes configurations
  - **Business Process Architect** (Plan agent) - Designs implementations
  - **Operations Manager** (general-purpose agent) - Executes workflows

- **Autonomous Operation**: Scheduled workflows run automatically
- **Natural Language Tasks**: Assign tasks in plain language
- **ERPNext Integration**: Direct API access to your ERP

## Quick Start (5 Minutes)

### Step 1: Set Environment Variables

Copy `agent-setup/env.example` to `agent-setup/.env`:

```bash
cd agent-setup
cp env.example .env
```

Edit `.env` and set:

```env
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
CLAUDE_API_KEY=your_claude_key
```

### Step 2: Install Dependencies

```bash
# Make sure you're in agent-setup directory
cd agent-setup

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Run the Quick Start

```bash
python start_subagent_system.py
```

This will:
- ✓ Check prerequisites
- ✓ Initialize the subagent bridge
- ✓ Create default AI employees
- ✓ Demonstrate task assignment
- ✓ Show autonomous workflows

### Step 4: Try Examples

```bash
python subagent_examples.py
```

Choose from 6 interactive examples demonstrating different capabilities.

## Basic Usage

### Example 1: Assign a Task to System Analyst

```python
from claude_code_bridge import SubagentERPNextBridge

# Initialize
bridge = SubagentERPNextBridge(erpnext_base_url="http://localhost:8000")

# Get the System Analyst employee
analyst = bridge.get_employee_by_type("Explore")

# Assign exploration task
task = bridge.assign_task(
    employee_id=analyst.employee_id,
    task_description="""
    Explore the ERPNext Sales module:
    1. List all custom fields in Sales Order
    2. Find custom print formats
    3. Document workflow states
    """
)

# Get the prompt for Claude Code
prompt = bridge.get_task_prompt(task)

# In Claude Code, use: Task tool with this prompt
print(task.task_id)
```

### Example 2: Use the Autonomous Orchestrator

```python
from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator

# Initialize
orchestrator = EnhancedAutonomousOrchestrator(
    erpnext_base_url="http://localhost:8000"
)

# Delegate a task (auto-detects type)
result = orchestrator.delegate_to_subagent(
    task_description="Find all customers created this month",
    task_type="auto"  # Will detect this is an 'explore' task
)

print(f"Assigned to: {result['employee_name']}")
print(f"Task ID: {result['task_id']}")
```

### Example 3: Execute an Autonomous Workflow

```python
# Execute a registered workflow
result = orchestrator.execute_workflow("daily_health_check")

print(f"Workflow: {result['workflow_name']}")
print(f"Executed: {result['execution_time']}")
```

## Default AI Employees

### 1. Sarah Al-Mutairi - System Analyst
- **Type**: Explore agent
- **Department**: IT
- **Capabilities**:
  - Codebase exploration
  - Configuration analysis
  - Workflow mapping
  - Doctype analysis

**Example Tasks**:
```
"Explore all custom fields in Customer doctype"
"Map the sales order approval workflow"
"Find all custom scripts in the Sales module"
```

### 2. Mohammed Al-Ahmad - Business Process Architect
- **Type**: Plan agent
- **Department**: Operations
- **Capabilities**:
  - Process design
  - Implementation planning
  - Risk assessment
  - Architecture design

**Example Tasks**:
```
"Plan implementation of a commission calculation system"
"Design a multi-company consolidation process"
"Create a plan for customer loyalty program"
```

### 3. Fatima Al-Saud - Operations Manager
- **Type**: general-purpose agent
- **Department**: Sales
- **Capabilities**:
  - Workflow execution
  - Bulk processing
  - Report generation
  - Multi-module coordination

**Example Tasks**:
```
"Generate all pending invoices and email them"
"Process monthly sales closing workflow"
"Create 50 items from this spreadsheet"
```

## Default Autonomous Workflows

The system comes with 4 pre-configured workflows:

1. **Daily System Health Check** (9:00 AM)
   - Checks configuration errors
   - Reviews system logs
   - Verifies module functionality

2. **Weekly Process Optimization** (Monday)
   - Analyzes workflow performance
   - Identifies bottlenecks
   - Suggests improvements

3. **Monthly Sales Closing** (Last day of month)
   - Generates invoices
   - Sends payment reminders
   - Creates reports

4. **Customer Follow-up** (Daily 10:00 AM)
   - Follows up on pending quotations
   - Sends reminder emails
   - Updates statuses

## Using in Claude Code

When you get a task from the bridge, use Claude Code's Task tool:

```python
# In your code
task = bridge.assign_task(employee_id="...", task_description="...")
prompt = bridge.get_task_prompt(task)

# Then in Claude Code:
# Task(
#     subagent_type="Explore",  # or "Plan" or "general-purpose"
#     description="Brief task description",
#     prompt=prompt
# )
```

The subagent will execute using its specialized capabilities and return results.

## Create Custom Employees

```python
# Create a specialized Inventory employee
inventory_specialist = bridge.create_operations_employee(
    employee_name="Khaled Al-Rashid",
    department="Warehouse Operations"
)

# Assign inventory tasks
task = bridge.assign_task(
    employee_id=inventory_specialist.employee_id,
    task_description="""
    Check stock levels for all warehouses
    Generate purchase requests for low-stock items
    Create daily inventory report
    """
)
```

## Create Custom Workflows

```python
orchestrator.create_custom_workflow(
    workflow_id="inventory_restock",
    name="Automated Inventory Restocking",
    description="Check inventory and create purchase requests",
    task_description="""
    1. Check all warehouses for items below reorder level
    2. Generate purchase requests
    3. Email requests to procurement team
    """,
    task_type="execute",
    schedule="daily_8am"
)
```

## Monitoring

### Check System Status

```python
status = bridge.get_system_status()
print(json.dumps(status, indent=2))
```

### View Employees

```python
employees = bridge.list_employees()
for emp in employees:
    print(f"{emp.employee_name} - {emp.role} ({emp.status})")
```

### View Task History

```python
tasks = bridge.get_task_history(status="completed")
for task in tasks:
    print(f"{task.task_id}: {task.employee_name} - {task.status}")
```

## Integration with Existing System

The subagent bridge integrates seamlessly with your existing:

- ✓ **Employee Agent System** (`employee-agent-system.py`)
- ✓ **Autonomous Orchestrator** (`autonomous-orchestrator.py`)
- ✓ **Multi-tenant System** (`tenant-manager.py`)
- ✓ **ERPNext Integration** (All existing APIs)

## File Structure

```
agent-setup/
├── claude_code_bridge.py              # Core bridge implementation
├── enhanced_autonomous_orchestrator.py # Enhanced orchestrator
├── subagent_examples.py               # Usage examples
├── start_subagent_system.py          # Quick start script
├── requirements_subagents.txt         # Dependencies
└── .env                               # Configuration
```

## Troubleshooting

### Import Errors

```bash
# Make sure you're in agent-setup directory
cd agent-setup

# Reinstall dependencies
pip install -r requirements.txt
```

### Connection Errors

- Verify ERPNext is running: `http://localhost:8000`
- Check API credentials in `.env`
- Ensure user has proper permissions

### No Employees Available

```python
# Employees are created automatically on bridge initialization
# To recreate:
bridge = SubagentERPNextBridge(erpnext_base_url="...")
# Default employees are created in __init__
```

## Next Steps

1. ✓ Run `python start_subagent_system.py`
2. ✓ Try examples: `python subagent_examples.py`
3. ✓ Read full documentation: `CLAUDE_CODE_SUBAGENTS_AS_EMPLOYEES.md`
4. ✓ Create custom employees for your needs
5. ✓ Set up autonomous workflows
6. ✓ Integrate with your application

## Support

- Full Documentation: [CLAUDE_CODE_SUBAGENTS_AS_EMPLOYEES.md](../CLAUDE_CODE_SUBAGENTS_AS_EMPLOYEES.md)
- ERPNext Docs: https://docs.erpnext.com/
- Claude Code: https://github.com/anthropics/claude-code

---

**Your ERP is now managed by AI employees!** 🚀
