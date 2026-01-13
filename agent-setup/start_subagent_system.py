"""
Quick Start Script for Claude Code Subagent ERP Employee System
Run this to initialize and test the subagent integration
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from claude_code_bridge import SubagentERPNextBridge
from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator


def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


def check_prerequisites():
    """Check if all prerequisites are met"""
    print_header("CHECKING PREREQUISITES")

    prerequisites = {
        "ERPNEXT_BASE_URL": os.getenv("ERPNEXT_BASE_URL"),
        "ERPNEXT_API_KEY": os.getenv("ERPNEXT_API_KEY"),
        "ERPNEXT_API_SECRET": os.getenv("ERPNEXT_API_SECRET"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY")
    }

    all_ok = True
    for key, value in prerequisites.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}: {'[SET]' if value else '[NOT SET]'}")
        if not value:
            all_ok = False

    print()

    if not all_ok:
        print("❌ Missing required environment variables!")
        print("\nPlease set the following in your .env file:")
        print("  - ERPNEXT_BASE_URL")
        print("  - ERPNEXT_API_KEY")
        print("  - ERPNEXT_API_SECRET")
        print("  - CLAUDE_API_KEY")
        print("\nSee env.example for reference.")
        return False

    print("✓ All prerequisites met!")
    return True


def initialize_subagent_bridge():
    """Initialize the Claude Code subagent bridge"""
    print_header("INITIALIZING SUBAGENT BRIDGE")

    erpnext_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")

    print(f"ERPNext URL: {erpnext_url}")
    print("Creating subagent bridge...")

    bridge = SubagentERPNextBridge(erpnext_base_url=erpnext_url)

    print(f"✓ Bridge initialized with {len(bridge.employees)} employees")
    print()

    return bridge


def display_employees(bridge: SubagentERPNextBridge):
    """Display all subagent employees"""
    print_header("SUBAGENT EMPLOYEES")

    employees = bridge.list_employees()

    for emp in employees:
        print(f"👤 {emp.employee_name}")
        print(f"   Role: {emp.role}")
        print(f"   Department: {emp.department}")
        print(f"   Type: {emp.subagent_type}")
        print(f"   Status: {emp.status}")
        print(f"   Capabilities: {len(emp.capabilities)} capabilities")
        print()


def demonstrate_task_assignment(bridge: SubagentERPNextBridge):
    """Demonstrate task assignment to subagents"""
    print_header("TASK ASSIGNMENT DEMONSTRATION")

    # Get an explorer employee
    explorer = bridge.get_employee_by_type("Explore")

    if explorer:
        print(f"Assigning exploration task to: {explorer.employee_name}")
        print()

        task = bridge.assign_task(
            employee_id=explorer.employee_id,
            task_description="""
            Explore the ERPNext Sales module:
            1. List all doctypes in the Sales module
            2. Identify custom fields in Sales Order
            3. Find any custom scripts
            """
        )

        print(f"✓ Task assigned: {task.task_id}")
        print(f"  Employee: {task.employee_name}")
        print(f"  Status: {task.status}")
        print()

        # Show the prompt that would be used
        print("Subagent Prompt Preview:")
        print("-" * 80)
        prompt = bridge.get_task_prompt(task)
        print(prompt[:400] + "...\n")
        print("-" * 80)
        print()

        print("In Claude Code, you would execute this with:")
        print(f"  Task tool, subagent_type='{task.subagent_type}'")
        print()

        return task
    else:
        print("❌ No explorer employee available")
        return None


def demonstrate_orchestrator():
    """Demonstrate the enhanced autonomous orchestrator"""
    print_header("ENHANCED AUTONOMOUS ORCHESTRATOR")

    erpnext_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    orchestrator = EnhancedAutonomousOrchestrator(erpnext_base_url=erpnext_url)

    print(f"Orchestrator initialized with ERPNext at: {erpnext_url}")
    print()

    # Show registered workflows
    print("Registered Autonomous Workflows:")
    print("-" * 80)

    for wf_id, workflow in orchestrator.autonomous_workflows.items():
        print(f"\n  {workflow['name']}")
        print(f"    ID: {wf_id}")
        print(f"    Schedule: {workflow['schedule']}")
        print(f"    Subagent: {workflow['subagent_type']}")
        print(f"    Status: {'Enabled' if workflow['enabled'] else 'Disabled'}")

    print()

    # Demonstrate task delegation
    print("\nDemonstrating Auto Task Delegation:")
    print("-" * 80)

    task = orchestrator.delegate_to_subagent(
        task_description="Explore current customer management configuration",
        task_type="auto"  # Auto-detect task type
    )

    print(f"✓ Task delegated automatically")
    print(f"  Detected type: explore")
    print(f"  Assigned to: {task['employee_name']} ({task['employee_role']})")
    print(f"  Task ID: {task['task_id']}")
    print()

    return orchestrator


def show_usage_guide():
    """Show usage guide"""
    print_header("USAGE GUIDE")

    print("""
HOW TO USE THE SUBAGENT SYSTEM:

1. DIRECT SUBAGENT USAGE (via bridge):
   ------------------------------------------
   from claude_code_bridge import SubagentERPNextBridge

   bridge = SubagentERPNextBridge(erpnext_base_url="...")

   # Get an employee
   employee = bridge.get_employee_by_type("Explore")

   # Assign a task
   task = bridge.assign_task(
       employee_id=employee.employee_id,
       task_description="Your task here..."
   )

   # Get the prompt for Claude Code
   prompt = bridge.get_task_prompt(task)

   # In Claude Code, use the Task tool with this prompt


2. ORCHESTRATOR USAGE (autonomous workflows):
   ------------------------------------------
   from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator

   orchestrator = EnhancedAutonomousOrchestrator(erpnext_base_url="...")

   # Delegate a task (auto-detects type)
   result = orchestrator.delegate_to_subagent(
       task_description="Your task here...",
       task_type="auto"
   )

   # Execute a registered workflow
   result = orchestrator.execute_workflow("daily_health_check")

   # Create custom workflow
   orchestrator.create_custom_workflow(
       workflow_id="my_workflow",
       name="My Custom Workflow",
       description="...",
       task_description="...",
       task_type="execute"
   )


3. EXAMPLES:
   ------------------------------------------
   Run the examples script:
     python subagent_examples.py

   See examples for:
   - Exploring ERPNext configuration
   - Planning implementations
   - Executing workflows
   - Coordinating multiple subagents


4. IN CLAUDE CODE:
   ------------------------------------------
   When you get a task prompt from the bridge or orchestrator,
   use Claude Code's Task tool:

   Task(
       subagent_type="Explore",  # or "Plan" or "general-purpose"
       description="Brief description",
       prompt="[The full prompt from bridge.get_task_prompt()]"
   )

   The subagent will execute using its specialized capabilities
   and return results.


5. MONITORING:
   ------------------------------------------
   # Get system status
   status = bridge.get_system_status()
   print(json.dumps(status, indent=2))

   # View task history
   tasks = bridge.get_task_history()

   # View employee roster
   employees = bridge.list_employees()


6. AUTONOMOUS OPERATION:
   ------------------------------------------
   The orchestrator can run scheduled workflows automatically.
   Set up cron jobs or use a task scheduler to call:

   orchestrator.run_scheduled_workflows()

   This will execute all workflows that are due to run.
    """)


def save_demo_state(bridge: SubagentERPNextBridge, orchestrator: EnhancedAutonomousOrchestrator):
    """Save the current state"""
    print_header("SAVING STATE")

    # Save bridge state
    bridge.save_state("demo_subagent_state.json")
    print("✓ Subagent bridge state saved to: demo_subagent_state.json")

    # Save system overview
    overview = orchestrator.get_system_overview()
    with open("demo_system_overview.json", 'w', encoding='utf-8') as f:
        json.dump(overview, f, indent=2, ensure_ascii=False)
    print("✓ System overview saved to: demo_system_overview.json")
    print()


def main():
    """Main entry point"""
    print_header("CLAUDE CODE SUBAGENT ERP EMPLOYEE SYSTEM")
    print("Quick Start & Demonstration")
    print()

    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)

    # Initialize bridge
    bridge = initialize_subagent_bridge()

    # Display employees
    display_employees(bridge)

    # Demonstrate task assignment
    task = demonstrate_task_assignment(bridge)

    # Demonstrate orchestrator
    orchestrator = demonstrate_orchestrator()

    # Show usage guide
    show_usage_guide()

    # Save demo state
    save_demo_state(bridge, orchestrator)

    # Final summary
    print_header("SETUP COMPLETE!")

    print("""
✓ Claude Code Subagent Bridge initialized
✓ Default employees created
✓ Enhanced Autonomous Orchestrator ready
✓ Example tasks demonstrated

NEXT STEPS:

1. Review the generated files:
   - demo_subagent_state.json (current state)
   - demo_system_overview.json (system overview)

2. Run examples:
   python subagent_examples.py

3. Integrate with your workflows:
   - Import claude_code_bridge in your code
   - Use enhanced_autonomous_orchestrator for automation

4. In Claude Code:
   - Use Task tool with generated prompts
   - Leverage specialized subagents (Explore, Plan, general-purpose)

5. Read the documentation:
   - CLAUDE_CODE_SUBAGENTS_AS_EMPLOYEES.md

Happy automating with AI employees! 🚀
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
