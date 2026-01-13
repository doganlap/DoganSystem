"""
Example usage of Claude Code Subagent Bridge
Demonstrates how to use subagents as ERP employees
"""

import os
import json
from claude_code_bridge import SubagentERPNextBridge


def example_1_explore_sales_module():
    """
    Example 1: Use Explorer agent to analyze Sales module
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Explore Sales Module Configuration")
    print("="*70 + "\n")

    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Get the System Analyst (Explorer)
    analyst = bridge.get_employee_by_role("System Analyst")

    if analyst:
        print(f"Assigned to: {analyst.employee_name} ({analyst.role})")
        print(f"Department: {analyst.department}")
        print()

        # Assign exploration task
        task = bridge.assign_task(
            employee_id=analyst.employee_id,
            task_description="""
            Explore the ERPNext Sales module and provide a comprehensive report:

            1. Custom Fields Analysis:
               - List all custom fields added to Sales Order doctype
               - List all custom fields added to Quotation doctype
               - Document field types and purposes

            2. Print Formats:
               - Find all custom print formats for quotations
               - Find all custom print formats for sales orders

            3. Workflows:
               - Map the sales order approval workflow
               - Document workflow states and transitions

            4. Custom Scripts:
               - Identify all client scripts in Sales module
               - Identify all server scripts

            Please provide detailed findings with file paths where applicable.
            """
        )

        print(f"Task ID: {task.task_id}")
        print(f"Status: {task.status}")
        print()

        # Generate the full prompt that would be sent to the subagent
        prompt = bridge.get_task_prompt(task)

        print("Generated Prompt for Claude Code Subagent:")
        print("-" * 70)
        print(prompt)
        print("-" * 70)

        print("\nNOTE: In Claude Code, you would now use the Task tool with:")
        print(f"  subagent_type: '{task.subagent_type}'")
        print(f"  prompt: [the prompt above]")
        print()

        return task
    else:
        print("No System Analyst available")
        return None


def example_2_plan_commission_system():
    """
    Example 2: Use Planner agent to design commission system
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Plan Sales Commission System Implementation")
    print("="*70 + "\n")

    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Get the Business Process Architect (Planner)
    architect = bridge.get_employee_by_role("Business Process Architect")

    if architect:
        print(f"Assigned to: {architect.employee_name} ({architect.role})")
        print(f"Department: {architect.department}")
        print()

        # Assign planning task
        task = bridge.assign_task(
            employee_id=architect.employee_id,
            task_description="""
            Plan the implementation of a comprehensive sales commission system:

            REQUIREMENTS:
            1. Commission Calculation:
               - Calculate commissions based on achieved sales targets
               - Support tiered commission rates (e.g., 3% for 0-100K, 5% for 100K-500K, 7% for 500K+)
               - Handle both individual and team-based commissions

            2. Integration:
               - Integrate with Sales Order and Sales Invoice modules
               - Connect to HR Payroll module for payment processing
               - Support commission adjustments and corrections

            3. Reporting:
               - Monthly commission reports per salesperson
               - Team commission summaries
               - Commission forecasting based on pipeline

            DELIVERABLES REQUIRED:
            1. Detailed implementation plan with phases
            2. Custom DocTypes needed (with field specifications)
            3. Custom fields to add to existing DocTypes
            4. Workflow design
            5. Server scripts and automation logic
            6. Report specifications
            7. Data migration strategy (if applicable)
            8. Testing approach and test cases
            9. Risk assessment and mitigation strategies
            10. Timeline estimates for each phase

            Please provide a comprehensive, actionable plan following ERPNext best practices.
            """
        )

        print(f"Task ID: {task.task_id}")
        print(f"Status: {task.status}")
        print()

        # Generate the full prompt
        prompt = bridge.get_task_prompt(task)

        print("Generated Prompt for Claude Code Subagent:")
        print("-" * 70)
        print(prompt[:800] + "\n... [truncated] ...")
        print("-" * 70)

        print("\nNOTE: In Claude Code, you would now use the Task tool with:")
        print(f"  subagent_type: '{task.subagent_type}'")
        print(f"  description: 'Plan commission system implementation'")
        print()

        return task
    else:
        print("No Business Process Architect available")
        return None


def example_3_execute_monthly_closing():
    """
    Example 3: Use Operations agent to execute monthly closing process
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Execute Monthly Sales Closing Process")
    print("="*70 + "\n")

    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Get the Operations Manager
    operator = bridge.get_employee_by_role("Operations Manager")

    if operator:
        print(f"Assigned to: {operator.employee_name} ({operator.role})")
        print(f"Department: {operator.department}")
        print()

        # Assign execution task
        task = bridge.assign_task(
            employee_id=operator.employee_id,
            task_description="""
            Execute the monthly sales closing process for the current month:

            WORKFLOW STEPS:
            1. Data Collection:
               - Retrieve all completed Sales Orders from this month
               - Identify Sales Orders with pending invoices
               - List all draft invoices

            2. Invoice Generation:
               - Generate invoices for all delivered Sales Orders without invoices
               - Validate invoice amounts against Sales Orders
               - Submit all draft invoices that are validated

            3. Payment Processing:
               - Check for received payments not yet reconciled
               - Match payments to invoices
               - Update payment status

            4. Follow-up Actions:
               - Identify invoices overdue by more than 30 days
               - Generate payment reminder emails
               - Send reminders to customers

            5. Reporting:
               - Generate monthly sales summary report
               - Create accounts receivable aging report
               - Compile commission calculation data
               - Email reports to: sales@company.com, finance@company.com

            6. Validation & Logging:
               - Verify all invoices are properly booked
               - Check for any errors or exceptions
               - Log all actions taken
               - Create summary of operations performed

            IMPORTANT:
            - Validate all data before making changes
            - Handle errors gracefully and report them
            - Do not send actual emails (log email content instead)
            - Provide detailed execution report

            Execute this workflow using ERPNext API and report results.
            """
        )

        print(f"Task ID: {task.task_id}")
        print(f"Status: {task.status}")
        print()

        # Generate the full prompt
        prompt = bridge.get_task_prompt(task)

        print("Generated Prompt for Claude Code Subagent:")
        print("-" * 70)
        print(prompt[:800] + "\n... [truncated] ...")
        print("-" * 70)

        print("\nNOTE: In Claude Code, you would now use the Task tool with:")
        print(f"  subagent_type: '{task.subagent_type}'")
        print(f"  description: 'Execute monthly sales closing'")
        print()

        return task
    else:
        print("No Operations Manager available")
        return None


def example_4_coordinated_workflow():
    """
    Example 4: Coordinated workflow using multiple subagents
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Coordinated Multi-Agent Workflow")
    print("="*70 + "\n")

    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    print("SCENARIO: Implement a new customer loyalty program")
    print()

    # Step 1: Explore current setup
    print("STEP 1: Explore Current System")
    print("-" * 40)
    analyst = bridge.get_employee_by_type("Explore")
    if analyst:
        task1 = bridge.assign_task(
            employee_id=analyst.employee_id,
            task_description="Explore current customer management setup, identify where loyalty data could be stored, and analyze existing customer fields."
        )
        print(f"  Assigned to: {analyst.employee_name}")
        print(f"  Task: {task1.task_id}")
    print()

    # Step 2: Plan implementation
    print("STEP 2: Plan Implementation")
    print("-" * 40)
    architect = bridge.get_employee_by_type("Plan")
    if architect:
        task2 = bridge.assign_task(
            employee_id=architect.employee_id,
            task_description="Based on exploration findings, plan a points-based customer loyalty program with reward tiers, point accumulation, and redemption process."
        )
        print(f"  Assigned to: {architect.employee_name}")
        print(f"  Task: {task2.task_id}")
    print()

    # Step 3: Execute implementation
    print("STEP 3: Execute Implementation")
    print("-" * 40)
    operator = bridge.get_employee_by_type("general-purpose")
    if operator:
        task3 = bridge.assign_task(
            employee_id=operator.employee_id,
            task_description="Implement the planned loyalty program by creating custom fields, setting up automation, and testing the system."
        )
        print(f"  Assigned to: {operator.employee_name}")
        print(f"  Task: {task3.task_id}")
    print()

    print("This demonstrates a complete workflow:")
    print("  1. Explore (understand current state)")
    print("  2. Plan (design the solution)")
    print("  3. Execute (implement the plan)")
    print()


def example_5_system_status():
    """
    Example 5: Check system status and employee availability
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: System Status and Employee Management")
    print("="*70 + "\n")

    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Get system status
    status = bridge.get_system_status()

    print("SYSTEM STATUS:")
    print("-" * 40)
    print(json.dumps(status, indent=2))
    print()

    # List all employees
    print("EMPLOYEE ROSTER:")
    print("-" * 40)
    employees = bridge.list_employees()
    for emp in employees:
        print(f"\n  {emp.employee_name}")
        print(f"    ID: {emp.employee_id}")
        print(f"    Role: {emp.role}")
        print(f"    Department: {emp.department}")
        print(f"    Type: {emp.subagent_type}")
        print(f"    Status: {emp.status}")
        print(f"    Capabilities ({len(emp.capabilities)}):")
        for cap in emp.capabilities:
            print(f"      - {cap}")
    print()

    # Task history
    print("TASK HISTORY:")
    print("-" * 40)
    tasks = bridge.get_task_history()
    if tasks:
        for task in tasks[-5:]:  # Last 5 tasks
            print(f"\n  Task {task.task_id}")
            print(f"    Employee: {task.employee_name}")
            print(f"    Status: {task.status}")
            print(f"    Created: {task.created_at}")
            if task.completed_at:
                print(f"    Completed: {task.completed_at}")
    else:
        print("  No tasks in history")
    print()


def example_6_custom_employee():
    """
    Example 6: Create a custom specialized employee
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Create Custom Specialized Employee")
    print("="*70 + "\n")

    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Create a custom Inventory Specialist
    inventory_specialist = bridge.create_operations_employee(
        employee_name="Khaled Al-Rashid",
        department="Warehouse Operations",
        employee_id="emp_inventory_specialist_001"
    )

    print(f"Created: {inventory_specialist.employee_name}")
    print(f"  Role: {inventory_specialist.role}")
    print(f"  Department: {inventory_specialist.department}")
    print(f"  Type: {inventory_specialist.subagent_type}")
    print()

    # Assign an inventory-specific task
    task = bridge.assign_task(
        employee_id=inventory_specialist.employee_id,
        task_description="""
        Perform daily inventory management tasks:

        1. Check stock levels for all warehouses
        2. Identify items below reorder level
        3. Generate purchase requests for low-stock items
        4. Review pending stock transfers
        5. Generate daily inventory report
        """
    )

    print(f"Task Assigned: {task.task_id}")
    print(f"Status: {task.status}")
    print()

    # Save the updated state
    bridge.save_state("custom_employees_state.json")
    print("State saved with custom employee")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("CLAUDE CODE SUBAGENT BRIDGE - EXAMPLES")
    print("="*70)

    # Check environment variables
    if not os.getenv("ERPNEXT_BASE_URL"):
        print("\nWARNING: ERPNEXT_BASE_URL not set in environment")
        print("Using default: http://localhost:8000")
        print()

    # Run examples
    examples = [
        ("1", "Explore Sales Module", example_1_explore_sales_module),
        ("2", "Plan Commission System", example_2_plan_commission_system),
        ("3", "Execute Monthly Closing", example_3_execute_monthly_closing),
        ("4", "Coordinated Workflow", example_4_coordinated_workflow),
        ("5", "System Status", example_5_system_status),
        ("6", "Custom Employee", example_6_custom_employee),
    ]

    print("Available Examples:")
    for num, title, _ in examples:
        print(f"  {num}. {title}")

    print("\nEnter example number (1-6) or 'all' to run all examples:")
    print("(Press Enter to run all)")
    choice = input("> ").strip() or "all"

    if choice.lower() == "all":
        for num, title, func in examples:
            func()
    elif choice in [num for num, _, _ in examples]:
        for num, title, func in examples:
            if num == choice:
                func()
                break
    else:
        print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    main()
