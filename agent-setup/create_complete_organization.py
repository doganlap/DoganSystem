"""
Complete ERPNext Organization Setup
Creates full organizational chart with all employees and workflows
"""

import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import modules
from claude_code_bridge import SubagentERPNextBridge
from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator
from erpnext_org_chart import ERPNextOrgChart
from org_chart_workflows import ModuleWorkflows


def print_header(title: str, width: int = 80):
    """Print formatted header"""
    print("\n" + "="*width)
    print(title.center(width))
    print("="*width + "\n")


def check_prerequisites():
    """Check prerequisites"""
    print_header("CHECKING PREREQUISITES")

    required_vars = {
        "ERPNEXT_BASE_URL": os.getenv("ERPNEXT_BASE_URL"),
        "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY")
    }

    all_ok = True
    for key, value in required_vars.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}: {'[SET]' if value else '[NOT SET]'}")
        if not value:
            all_ok = False

    print()

    if not all_ok:
        print("❌ Missing required environment variables!")
        print("\nPlease set in your .env file:")
        for key in required_vars:
            if not required_vars[key]:
                print(f"  - {key}")
        return False

    print("✓ All prerequisites met!")
    return True


def create_organization():
    """Create complete organization"""
    print_header("CREATING COMPLETE ERPNEXT ORGANIZATION")

    erpnext_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")

    print(f"ERPNext URL: {erpnext_url}")
    print("Initializing subagent bridge...")

    # Create bridge
    bridge = SubagentERPNextBridge(erpnext_base_url=erpnext_url)
    print(f"✓ Bridge initialized")

    # Create organizational chart
    print("\nCreating organizational chart...")
    org_chart = ERPNextOrgChart(bridge)
    summary = org_chart.create_complete_org_chart()

    print(f"✓ Organizational chart created")
    print(f"  Total Employees: {summary['total_employees']}")
    print(f"  Total Departments: {summary['total_departments']}")

    return bridge, org_chart


def register_workflows(orchestrator: EnhancedAutonomousOrchestrator):
    """Register all module workflows"""
    print_header("REGISTERING MODULE WORKFLOWS")

    all_workflows = ModuleWorkflows.get_all_workflows()

    total_registered = 0
    for module, workflows in all_workflows.items():
        print(f"\n{module} Module:")
        for wf in workflows:
            orchestrator.register_workflow(
                workflow_id=wf["workflow_id"],
                name=wf["name"],
                description=f"{module} - {wf['name']}",
                schedule=wf["schedule"],
                subagent_type=wf["subagent_type"],
                task_template=wf["task"]
            )
            total_registered += 1
            print(f"  ✓ {wf['name']}")

    print(f"\n✓ Total workflows registered: {total_registered}")
    return total_registered


def generate_visualizations(org_chart: ERPNextOrgChart, bridge: SubagentERPNextBridge):
    """Generate visualization files"""
    print_header("GENERATING VISUALIZATIONS")

    # Generate text org chart
    print("Generating text organizational chart...")
    text_chart = org_chart.generate_org_chart_text()
    with open("org_chart_visualization.txt", 'w', encoding='utf-8') as f:
        f.write(text_chart)
    print("✓ org_chart_visualization.txt")

    # Save JSON org chart
    print("Saving JSON organizational chart...")
    org_chart.save_org_chart("erpnext_complete_org_chart.json")
    print("✓ erpnext_complete_org_chart.json")

    # Save employee state
    print("Saving employee state...")
    bridge.save_state("complete_org_employees.json")
    print("✓ complete_org_employees.json")

    # Generate workflow summary
    print("Generating workflow summary...")
    workflow_summary = ModuleWorkflows.get_workflow_summary()
    with open("workflow_summary.json", 'w', encoding='utf-8') as f:
        json.dump(workflow_summary, f, indent=2, ensure_ascii=False)
    print("✓ workflow_summary.json")

    # Generate HTML visualization
    print("Generating HTML visualization...")
    generate_html_visualization(org_chart)
    print("✓ org_chart.html")


def generate_html_visualization(org_chart: ERPNextOrgChart):
    """Generate HTML visualization of org chart"""
    html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERPNext Organizational Chart</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .summary {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            text-align: center;
            min-width: 150px;
            margin: 10px;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            display: block;
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        .departments {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .department-card {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            background: #fafafa;
        }
        .department-card h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .employee {
            background: white;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        .employee-name {
            font-weight: bold;
            color: #2c3e50;
        }
        .employee-title {
            font-size: 13px;
            color: #7f8c8d;
        }
        .employee-type {
            display: inline-block;
            margin-top: 5px;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }
        .type-explore { background: #e3f2fd; color: #1976d2; }
        .type-plan { background: #f3e5f5; color: #7b1fa2; }
        .type-ops { background: #e8f5e9; color: #388e3c; }
        .executive { background: #fff3e0; border-left-color: #ff9800; }
        @media print {
            body { background: white; }
            .container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 ERPNext Complete Organizational Chart</h1>
        <p style="text-align: center; color: #7f8c8d;">
            Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
        </p>

        <div class="summary">
"""

    summary = org_chart.get_org_chart_summary()

    html += f"""
            <div class="stat-card">
                <span class="stat-number">{summary['total_employees']}</span>
                <span class="stat-label">Total Employees</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['total_departments']}</span>
                <span class="stat-label">Departments</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['by_subagent_type']['Explore']}</span>
                <span class="stat-label">Analysts</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['by_subagent_type']['Plan']}</span>
                <span class="stat-label">Planners</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{summary['by_subagent_type']['general-purpose']}</span>
                <span class="stat-label">Operations</span>
            </div>
        </div>

        <div class="departments">
"""

    # Group employees by department
    employees_by_dept = {}
    for emp_id, emp_data in org_chart.employee_registry.items():
        dept = emp_data["employee"].department
        if dept not in employees_by_dept:
            employees_by_dept[dept] = []
        employees_by_dept[dept].append(emp_data)

    for dept in sorted(employees_by_dept.keys()):
        employees = employees_by_dept[dept]
        html += f"""
            <div class="department-card">
                <h3>{dept} ({len(employees)} employees)</h3>
"""
        for emp_data in employees:
            employee = emp_data["employee"]
            title = emp_data["title"]

            type_class = {
                "Explore": "type-explore",
                "Plan": "type-plan",
                "general-purpose": "type-ops"
            }.get(employee.subagent_type, "type-ops")

            extra_class = " executive" if dept == "Executive" else ""

            html += f"""
                <div class="employee{extra_class}">
                    <div class="employee-name">{employee.employee_name}</div>
                    <div class="employee-title">{title}</div>
                    <span class="employee-type {type_class}">{employee.subagent_type}</span>
                </div>
"""
        html += """
            </div>
"""

    html += """
        </div>
    </div>
</body>
</html>
"""

    with open("org_chart.html", 'w', encoding='utf-8') as f:
        f.write(html)


def print_summary_report(summary: Dict, total_workflows: int):
    """Print final summary report"""
    print_header("DEPLOYMENT SUMMARY")

    print("ORGANIZATION STATISTICS:")
    print("-" * 80)
    print(f"  Total AI Employees:        {summary['total_employees']}")
    print(f"  Total Departments:         {summary['total_departments']}")
    print(f"  Total Workflows:           {total_workflows}")
    print()

    print("EMPLOYEES BY ROLE:")
    print("-" * 80)
    for role, count in summary['by_role_type'].items():
        print(f"  {role.title():20} {count}")
    print()

    print("EMPLOYEES BY TYPE:")
    print("-" * 80)
    for stype, count in summary['by_subagent_type'].items():
        print(f"  {stype:20} {count}")
    print()

    print("EMPLOYEES BY DEPARTMENT:")
    print("-" * 80)
    for dept, count in sorted(summary['by_department'].items()):
        print(f"  {dept:20} {count}")
    print()

    print("FILES GENERATED:")
    print("-" * 80)
    files = [
        "erpnext_complete_org_chart.json",
        "complete_org_employees.json",
        "workflow_summary.json",
        "org_chart_visualization.txt",
        "org_chart.html"
    ]
    for f in files:
        print(f"  ✓ {f}")
    print()


def main():
    """Main entry point"""
    print_header("ERPNEXT COMPLETE ORGANIZATION CREATOR", 80)
    print("This will create a full organizational chart with AI employees")
    print("for every ERPNext module, plus all module-specific workflows.")
    print()

    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)

    # Create organization
    bridge, org_chart = create_organization()
    summary = org_chart.get_org_chart_summary()

    # Create orchestrator
    print_header("INITIALIZING ORCHESTRATOR")
    orchestrator = EnhancedAutonomousOrchestrator(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )
    print("✓ Orchestrator initialized")

    # Register workflows
    total_workflows = register_workflows(orchestrator)

    # Generate visualizations
    generate_visualizations(org_chart, bridge)

    # Print summary
    print_summary_report(summary, total_workflows)

    print_header("🎉 ORGANIZATION SETUP COMPLETE! 🎉")

    print("""
NEXT STEPS:

1. View the organization chart:
   - Text format:  org_chart_visualization.txt
   - HTML format:  org_chart.html (open in browser)
   - JSON format:  erpnext_complete_org_chart.json

2. Review workflows:
   - workflow_summary.json

3. Start using your AI organization:
   - All employees are ready to work
   - All workflows are registered
   - System is fully operational

4. Execute workflows:
   python -c "from enhanced_autonomous_orchestrator import *; ..."

5. Assign tasks to employees:
   python -c "from claude_code_bridge import *; ..."

Your ERPNext is now managed by a complete AI organization! 🚀
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
