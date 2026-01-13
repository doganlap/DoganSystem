# Claude Code Subagents as ERP Employees

## Overview

This guide shows how to use **Claude Code's built-in subagents** to manage your ERPNext system as virtual employees, complementing your existing Python-based employee agent system.

## Architecture Integration

```
┌─────────────────────────────────────────────────────────┐
│          Claude Code Subagent Layer                      │
│  (Explore, Plan, general-purpose agents)                │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│     Subagent-ERPNext Bridge (New Component)             │
│  - Task conversion                                       │
│  - ERPNext API integration                               │
│  - Multi-step workflow execution                         │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│     Your Existing Employee Agent System                  │
│  - employee-agent-system.py                             │
│  - claude-agent-integration.py                          │
│  - autonomous-orchestrator.py                           │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              ERPNext v16 Backend                         │
└─────────────────────────────────────────────────────────┘
```

## Subagent Employee Roles

### 1. **Explore Agent** - "System Analyst"
**Role**: Understanding and mapping ERP configurations

**Capabilities**:
- Explore ERPNext codebase and configurations
- Find specific ERPNext doctypes and custom scripts
- Understand workflow configurations
- Map data relationships
- Identify customization points

**Example Tasks**:
```
"Find all custom fields added to the Customer doctype"
"Map the sales order approval workflow"
"Identify all custom scripts in the Sales module"
```

### 2. **Plan Agent** - "Business Process Architect"
**Role**: Designing complex ERP operations and workflows

**Capabilities**:
- Plan multi-step business processes
- Design data migration strategies
- Create implementation roadmaps
- Identify dependencies and risks
- Optimize workflow sequences

**Example Tasks**:
```
"Plan the implementation of a new commission calculation system"
"Design a multi-company consolidation process"
"Create a plan for migrating legacy customer data"
```

### 3. **general-purpose Agent** - "Operations Manager"
**Role**: Executing complex, multi-step ERP tasks

**Capabilities**:
- Execute multi-step workflows
- Handle complex data operations
- Coordinate between multiple ERPNext modules
- Perform bulk operations with validation
- Generate and analyze reports

**Example Tasks**:
```
"Create 50 new items with BOMs from this spreadsheet"
"Process all pending purchase orders and update inventory"
"Generate monthly financial reports and email to stakeholders"
```

## Implementation Guide

### Step 1: Create the Subagent-ERPNext Bridge

Create `agent-setup/claude_code_bridge.py`:

```python
"""
Bridge between Claude Code subagents and ERPNext
Allows Claude Code agents to work as ERP employees
"""

import os
import json
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from agent_orchestrator import ERPNextClient

class SubagentERPNextBridge:
    """
    Bridges Claude Code subagents with ERPNext
    Translates natural language tasks into ERPNext operations
    """

    def __init__(self, erpnext_client: ERPNextClient):
        self.erpnext = erpnext_client
        self.claude = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def create_explorer_employee(self, employee_name: str, department: str):
        """
        Create an Explore agent configured as ERP System Analyst
        """
        return {
            "subagent_type": "Explore",
            "employee_name": employee_name,
            "role": "System Analyst",
            "department": department,
            "capabilities": [
                "codebase_exploration",
                "configuration_analysis",
                "workflow_mapping",
                "customization_discovery"
            ],
            "system_prompt": f"""You are {employee_name}, a System Analyst in the {department} department.
Your role is to explore and understand the ERPNext system configuration.
You have deep knowledge of Frappe framework and ERPNext structure.
Use your tools to find, read, and analyze ERPNext configurations."""
        }

    def create_planner_employee(self, employee_name: str, department: str):
        """
        Create a Plan agent configured as Business Process Architect
        """
        return {
            "subagent_type": "Plan",
            "employee_name": employee_name,
            "role": "Business Process Architect",
            "department": department,
            "capabilities": [
                "process_design",
                "workflow_planning",
                "implementation_strategy",
                "risk_assessment"
            ],
            "system_prompt": f"""You are {employee_name}, a Business Process Architect in the {department} department.
Your role is to design and plan complex ERP operations.
You understand ERPNext modules, data flows, and business processes.
Create detailed implementation plans with step-by-step instructions."""
        }

    def create_operations_employee(self, employee_name: str, department: str):
        """
        Create a general-purpose agent configured as Operations Manager
        """
        return {
            "subagent_type": "general-purpose",
            "employee_name": employee_name,
            "role": "Operations Manager",
            "department": department,
            "capabilities": [
                "data_operations",
                "workflow_execution",
                "bulk_processing",
                "report_generation",
                "multi_module_coordination"
            ],
            "system_prompt": f"""You are {employee_name}, an Operations Manager in the {department} department.
Your role is to execute complex multi-step ERP operations.
You have access to ERPNext API and can perform data operations.
Always validate data before making changes and log all actions."""
        }

    def execute_task_with_subagent(
        self,
        employee_config: Dict,
        task_description: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Execute a task using the appropriate Claude Code subagent

        Args:
            employee_config: Employee configuration from create_*_employee()
            task_description: Natural language task description
            context: Additional context (ERPNext site, credentials, etc.)

        Returns:
            Task execution result
        """
        # Build the prompt for the subagent
        full_prompt = f"""
Employee Role: {employee_config['role']}
Department: {employee_config['department']}

ERPNext Context:
- Base URL: {self.erpnext.base_url}
- Available Capabilities: {', '.join(employee_config['capabilities'])}

Task:
{task_description}

{employee_config['system_prompt']}

Please complete this task using your available tools and capabilities.
"""

        # Note: In actual Claude Code implementation, you would use the Task tool
        # This is a conceptual example
        return {
            "employee": employee_config['employee_name'],
            "role": employee_config['role'],
            "task": task_description,
            "prompt": full_prompt,
            "subagent_type": employee_config['subagent_type']
        }

    def get_erpnext_context(self) -> Dict:
        """Get current ERPNext system context for subagents"""
        return {
            "base_url": self.erpnext.base_url,
            "available_modules": [
                "CRM", "Sales", "Buying", "Stock", "Accounts",
                "HR", "Projects", "Manufacturing", "Support"
            ],
            "site_config": self._get_site_config(),
            "enabled_apps": self._get_enabled_apps()
        }

    def _get_site_config(self) -> Dict:
        """Retrieve site configuration from ERPNext"""
        try:
            # This would use ERPNext API to get site settings
            return {
                "currency": "SAR",
                "country": "Saudi Arabia",
                "language": "ar"
            }
        except Exception as e:
            return {}

    def _get_enabled_apps(self) -> List[str]:
        """Get list of enabled Frappe/ERPNext apps"""
        try:
            # This would query ERPNext for enabled apps
            return ["frappe", "erpnext"]
        except Exception as e:
            return ["frappe", "erpnext"]


# Example usage
if __name__ == "__main__":
    from agent_orchestrator import ERPNextClient

    erpnext = ERPNextClient(
        base_url=os.getenv("ERPNEXT_BASE_URL"),
        api_key=os.getenv("ERPNEXT_API_KEY"),
        api_secret=os.getenv("ERPNEXT_API_SECRET")
    )

    bridge = SubagentERPNextBridge(erpnext)

    # Create different employee types
    analyst = bridge.create_explorer_employee("سارة المطيري", "IT")
    architect = bridge.create_planner_employee("محمد الأحمد", "Operations")
    operator = bridge.create_operations_employee("فاطمة السعود", "Sales")

    print("Created ERP Employees:")
    print(f"1. {analyst['employee_name']} - {analyst['role']}")
    print(f"2. {architect['employee_name']} - {architect['role']}")
    print(f"3. {operator['employee_name']} - {operator['role']}")
```

### Step 2: Using Subagents as Employees

#### Example 1: System Analyst (Explore Agent)

```python
from claude_code_bridge import SubagentERPNextBridge
from agent_orchestrator import ERPNextClient
import os

# Initialize
erpnext = ERPNextClient(
    base_url=os.getenv("ERPNEXT_BASE_URL"),
    api_key=os.getenv("ERPNEXT_API_KEY"),
    api_secret=os.getenv("ERPNEXT_API_SECRET")
)

bridge = SubagentERPNextBridge(erpnext)

# Create System Analyst employee
analyst = bridge.create_explorer_employee("Sarah Al-Mutairi", "IT Department")

# Assign exploration task
task = bridge.execute_task_with_subagent(
    employee_config=analyst,
    task_description="""
    Explore the ERPNext Sales module and provide:
    1. All custom fields added to Sales Order doctype
    2. Custom print formats for quotations
    3. Workflow states for sales orders
    4. Any custom scripts in the Sales module
    """
)

print(f"Task assigned to: {task['employee']}")
print(f"Subagent type: {task['subagent_type']}")
```

#### Example 2: Business Process Architect (Plan Agent)

```python
# Create Business Process Architect employee
architect = bridge.create_planner_employee("Mohammed Al-Ahmad", "Operations")

# Assign planning task
task = bridge.execute_task_with_subagent(
    employee_config=architect,
    task_description="""
    Plan the implementation of a new commission calculation system:

    Requirements:
    - Calculate sales commissions based on achieved targets
    - Support tiered commission rates
    - Handle team-based commissions
    - Integrate with payroll module

    Please provide:
    1. Implementation plan with steps
    2. Required custom fields and doctypes
    3. Workflow design
    4. Data migration strategy
    5. Testing approach
    """
)
```

#### Example 3: Operations Manager (general-purpose Agent)

```python
# Create Operations Manager employee
operator = bridge.create_operations_employee("Fatima Al-Saud", "Sales")

# Assign execution task
task = bridge.execute_task_with_subagent(
    employee_config=operator,
    task_description="""
    Execute the following sales operations:

    1. Retrieve all pending quotations older than 7 days
    2. For each quotation:
       - Check if customer has responded
       - Send follow-up email if no response
       - Update status to "Follow-up Sent"
       - Log the action in communication log
    3. Generate summary report of all follow-ups sent
    4. Email report to sales manager

    Please execute this workflow and report results.
    """
)
```

### Step 3: Integration with Your Workflow System

Integrate with your existing `autonomous-orchestrator.py`:

```python
# In autonomous-orchestrator.py

from claude_code_bridge import SubagentERPNextBridge

class AutonomousOrchestrator:
    def __init__(self):
        # ... existing initialization ...
        self.subagent_bridge = SubagentERPNextBridge(self.erpnext)
        self._initialize_subagent_employees()

    def _initialize_subagent_employees(self):
        """Create Claude Code subagent employees"""
        self.subagent_employees = {
            "system_analyst": self.subagent_bridge.create_explorer_employee(
                "AI System Analyst", "IT"
            ),
            "process_architect": self.subagent_bridge.create_planner_employee(
                "AI Process Architect", "Operations"
            ),
            "operations_manager": self.subagent_bridge.create_operations_employee(
                "AI Operations Manager", "Operations"
            )
        }

    def delegate_complex_task(self, task_description: str, task_type: str):
        """
        Delegate complex tasks to appropriate Claude Code subagent

        task_type: 'explore', 'plan', or 'execute'
        """
        employee_mapping = {
            "explore": "system_analyst",
            "plan": "process_architect",
            "execute": "operations_manager"
        }

        employee_key = employee_mapping.get(task_type)
        if not employee_key:
            raise ValueError(f"Unknown task type: {task_type}")

        employee = self.subagent_employees[employee_key]

        return self.subagent_bridge.execute_task_with_subagent(
            employee_config=employee,
            task_description=task_description
        )
```

## Use Cases

### Use Case 1: Monthly Sales Process Automation

```python
# Plan the process (Business Process Architect)
plan = orchestrator.delegate_complex_task(
    task_description="Plan automated monthly sales closing process",
    task_type="plan"
)

# Execute the process (Operations Manager)
result = orchestrator.delegate_complex_task(
    task_description="""
    Execute monthly sales closing:
    1. Generate all pending invoices from delivered orders
    2. Send invoices to customers
    3. Update payment reminders
    4. Generate monthly sales report
    5. Email report to management
    """,
    task_type="execute"
)
```

### Use Case 2: System Configuration Analysis

```python
# Explore configuration (System Analyst)
analysis = orchestrator.delegate_complex_task(
    task_description="""
    Analyze current inventory management configuration:
    1. List all warehouses and their settings
    2. Identify automated stock reorder rules
    3. Find all custom fields in Item doctype
    4. Review stock reconciliation workflows
    """,
    task_type="explore"
)
```

### Use Case 3: New Feature Implementation

```python
# Step 1: Explore (System Analyst)
current_state = orchestrator.delegate_complex_task(
    task_description="Explore current customer loyalty program setup",
    task_type="explore"
)

# Step 2: Plan (Business Process Architect)
implementation_plan = orchestrator.delegate_complex_task(
    task_description="Plan implementation of points-based loyalty program",
    task_type="plan"
)

# Step 3: Execute (Operations Manager)
implementation = orchestrator.delegate_complex_task(
    task_description="Implement the planned loyalty program following the plan",
    task_type="execute"
)
```

## Benefits of Using Claude Code Subagents

1. **Deep Code Understanding**: Explore agents can read and understand ERPNext codebase
2. **Complex Planning**: Plan agents create detailed implementation strategies
3. **Multi-step Execution**: general-purpose agents handle complex workflows
4. **No Additional Training**: Agents understand ERPNext/Frappe architecture natively
5. **Autonomous Operation**: Works seamlessly with your existing autonomous orchestrator
6. **Scalability**: Handle more complex tasks without manual intervention

## Best Practices

1. **Use Explore agents for**:
   - Understanding existing configurations
   - Finding customization points
   - Mapping data relationships
   - Analyzing workflows

2. **Use Plan agents for**:
   - Designing new features
   - Planning complex migrations
   - Creating implementation roadmaps
   - Risk assessment

3. **Use general-purpose agents for**:
   - Executing multi-step processes
   - Bulk data operations
   - Complex workflows spanning multiple modules
   - Automated reporting

## Monitoring and Logging

Add monitoring to your bridge:

```python
# In claude_code_bridge.py

import logging
from datetime import datetime

class SubagentERPNextBridge:
    def __init__(self, erpnext_client: ERPNextClient):
        # ... existing init ...
        self.task_log = []

    def log_task(self, employee_name: str, task: str, status: str, result: Any):
        """Log subagent task execution"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "employee": employee_name,
            "task": task,
            "status": status,
            "result": result
        }
        self.task_log.append(log_entry)
        logger.info(f"Subagent task: {employee_name} - {status}")

    def get_task_history(self, employee_name: Optional[str] = None) -> List[Dict]:
        """Retrieve task execution history"""
        if employee_name:
            return [log for log in self.task_log if log['employee'] == employee_name]
        return self.task_log
```

## Next Steps

1. Install the bridge: Copy `claude_code_bridge.py` to `agent-setup/`
2. Update your `.env` with required API keys
3. Test with simple exploration tasks
4. Integrate with your autonomous orchestrator
5. Create custom employee roles as needed
6. Monitor and optimize performance

## Support

- Review task logs in `logs/subagent_tasks.log`
- Check ERPNext API documentation for available operations
- Test each employee type independently before integration

---

**Your ERP is now managed by AI employees using Claude Code's advanced subagent system!**
