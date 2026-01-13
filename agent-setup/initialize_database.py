"""
Database Initialization Script
Populates database with complete organizational structure
"""

import os
import uuid
import json
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import models
from database_models import (
    db, Employee, Department, Team, Role, Responsibility,
    Capability, EmployeeCapability, Workflow, EmployeeRole
)
from erpnext_org_chart import ERPNextOrgChart
from claude_code_bridge import SubagentERPNextBridge
from org_chart_workflows import ModuleWorkflows


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


def init_departments():
    """Initialize departments"""
    print("Creating departments...")

    session = db.get_session()

    departments_data = [
        {
            'department_id': 'dept_executive',
            'department_name': 'Executive',
            'department_name_ar': 'التنفيذية',
            'description': 'Executive leadership team'
        },
        {
            'department_id': 'dept_it',
            'department_name': 'IT',
            'department_name_ar': 'تقنية المعلومات',
            'description': 'Information Technology',
            'erpnext_module': 'IT'
        },
        {
            'department_id': 'dept_finance',
            'department_name': 'Finance',
            'department_name_ar': 'المالية',
            'description': 'Financial Accounting',
            'erpnext_module': 'Accounts'
        },
        {
            'department_id': 'dept_crm',
            'department_name': 'CRM',
            'department_name_ar': 'إدارة علاقات العملاء',
            'description': 'Customer Relationship Management',
            'erpnext_module': 'CRM'
        },
        {
            'department_id': 'dept_sales',
            'department_name': 'Sales',
            'department_name_ar': 'المبيعات',
            'description': 'Sales Management',
            'erpnext_module': 'Sales'
        },
        {
            'department_id': 'dept_procurement',
            'department_name': 'Procurement',
            'department_name_ar': 'المشتريات',
            'description': 'Procurement and Buying',
            'erpnext_module': 'Buying'
        },
        {
            'department_id': 'dept_inventory',
            'department_name': 'Inventory',
            'department_name_ar': 'المخزون',
            'description': 'Inventory Management',
            'erpnext_module': 'Stock'
        },
        {
            'department_id': 'dept_hr',
            'department_name': 'HR',
            'department_name_ar': 'الموارد البشرية',
            'description': 'Human Resources',
            'erpnext_module': 'HR'
        },
        {
            'department_id': 'dept_pmo',
            'department_name': 'PMO',
            'department_name_ar': 'مكتب إدارة المشاريع',
            'description': 'Project Management Office',
            'erpnext_module': 'Projects'
        },
        {
            'department_id': 'dept_manufacturing',
            'department_name': 'Manufacturing',
            'department_name_ar': 'التصنيع',
            'description': 'Production Management',
            'erpnext_module': 'Manufacturing'
        },
        {
            'department_id': 'dept_support',
            'department_name': 'Support',
            'department_name_ar': 'الدعم الفني',
            'description': 'Customer Support',
            'erpnext_module': 'Support'
        },
        {
            'department_id': 'dept_quality',
            'department_name': 'Quality',
            'department_name_ar': 'الجودة',
            'description': 'Quality Management',
            'erpnext_module': 'Quality'
        },
        {
            'department_id': 'dept_assets',
            'department_name': 'Assets',
            'department_name_ar': 'الأصول',
            'description': 'Asset Management',
            'erpnext_module': 'Assets'
        }
    ]

    for dept_data in departments_data:
        dept = Department(**dept_data, is_active=True)
        session.add(dept)

    session.commit()
    print(f"✓ Created {len(departments_data)} departments")
    session.close()


def init_roles():
    """Initialize roles and responsibilities"""
    print("Creating roles and responsibilities...")

    session = db.get_session()

    roles_data = [
        {
            'role_id': 'role_ceo',
            'role_name': 'CEO',
            'role_description': 'Chief Executive Officer - Overall strategic leadership',
            'level': 'C-Level',
            'can_approve_workflows': True,
            'can_manage_employees': True,
            'can_view_analytics': True
        },
        {
            'role_id': 'role_cto',
            'role_name': 'CTO',
            'role_description': 'Chief Technology Officer - Technology strategy',
            'level': 'C-Level',
            'can_approve_workflows': True,
            'can_manage_employees': True,
            'can_view_analytics': True
        },
        {
            'role_id': 'role_cfo',
            'role_name': 'CFO',
            'role_description': 'Chief Financial Officer - Financial oversight',
            'level': 'C-Level',
            'can_approve_workflows': True,
            'can_manage_employees': True,
            'can_view_analytics': True
        },
        {
            'role_id': 'role_coo',
            'role_name': 'COO',
            'role_description': 'Chief Operating Officer - Operations management',
            'level': 'C-Level',
            'can_approve_workflows': True,
            'can_manage_employees': True,
            'can_view_analytics': True
        },
        {
            'role_id': 'role_director',
            'role_name': 'Director',
            'role_description': 'Department Director - Strategic department leadership',
            'level': 'Director',
            'can_approve_workflows': True,
            'can_manage_employees': True,
            'can_view_analytics': True
        },
        {
            'role_id': 'role_manager',
            'role_name': 'Manager',
            'role_description': 'Team Manager - Team leadership and coordination',
            'level': 'Manager',
            'can_approve_workflows': True,
            'can_execute_tasks': True
        },
        {
            'role_id': 'role_team_lead',
            'role_name': 'Team Lead',
            'role_description': 'Team Lead - Lead team operations',
            'level': 'Lead',
            'can_execute_tasks': True
        },
        {
            'role_id': 'role_specialist',
            'role_name': 'Specialist',
            'role_description': 'Specialist - Execute specialized tasks',
            'level': 'Specialist',
            'can_execute_tasks': True
        },
        {
            'role_id': 'role_analyst',
            'role_name': 'Analyst',
            'role_description': 'Analyst - Analyze data and provide insights',
            'level': 'Analyst',
            'can_execute_tasks': True,
            'can_view_analytics': True
        }
    ]

    for role_data in roles_data:
        role = Role(**role_data)
        session.add(role)

    session.commit()
    print(f"✓ Created {len(roles_data)} roles")
    session.close()


def init_capabilities():
    """Initialize capability definitions"""
    print("Creating capabilities...")

    session = db.get_session()

    capabilities_data = [
        # CRM Capabilities
        {
            'capability_id': 'cap_lead_mgmt',
            'capability_name': 'Lead Management',
            'category': 'Business',
            'erpnext_module': 'CRM',
            'erpnext_doctype': 'Lead'
        },
        {
            'capability_id': 'cap_customer_mgmt',
            'capability_name': 'Customer Management',
            'category': 'Business',
            'erpnext_module': 'CRM',
            'erpnext_doctype': 'Customer'
        },
        # Sales Capabilities
        {
            'capability_id': 'cap_quotation',
            'capability_name': 'Quotation Management',
            'category': 'Business',
            'erpnext_module': 'Sales',
            'erpnext_doctype': 'Quotation'
        },
        {
            'capability_id': 'cap_sales_order',
            'capability_name': 'Sales Order Processing',
            'category': 'Business',
            'erpnext_module': 'Sales',
            'erpnext_doctype': 'Sales Order'
        },
        {
            'capability_id': 'cap_sales_invoice',
            'capability_name': 'Sales Invoice Management',
            'category': 'Business',
            'erpnext_module': 'Sales',
            'erpnext_doctype': 'Sales Invoice'
        },
        # Inventory Capabilities
        {
            'capability_id': 'cap_stock_mgmt',
            'capability_name': 'Stock Management',
            'category': 'Operational',
            'erpnext_module': 'Stock',
            'erpnext_doctype': 'Stock Entry'
        },
        {
            'capability_id': 'cap_warehouse_mgmt',
            'capability_name': 'Warehouse Management',
            'category': 'Operational',
            'erpnext_module': 'Stock',
            'erpnext_doctype': 'Warehouse'
        },
        # Finance Capabilities
        {
            'capability_id': 'cap_gl_posting',
            'capability_name': 'General Ledger Posting',
            'category': 'Financial',
            'erpnext_module': 'Accounts',
            'erpnext_doctype': 'Journal Entry'
        },
        {
            'capability_id': 'cap_payment_proc',
            'capability_name': 'Payment Processing',
            'category': 'Financial',
            'erpnext_module': 'Accounts',
            'erpnext_doctype': 'Payment Entry'
        },
        # Analytical Capabilities
        {
            'capability_id': 'cap_data_analysis',
            'capability_name': 'Data Analysis',
            'category': 'Analytical',
            'skill_level': 'Advanced'
        },
        {
            'capability_id': 'cap_reporting',
            'capability_name': 'Report Generation',
            'category': 'Analytical',
            'skill_level': 'Intermediate'
        },
        # Technical Capabilities
        {
            'capability_id': 'cap_system_config',
            'capability_name': 'System Configuration',
            'category': 'Technical',
            'skill_level': 'Advanced'
        },
        {
            'capability_id': 'cap_workflow_design',
            'capability_name': 'Workflow Design',
            'category': 'Technical',
            'skill_level': 'Advanced'
        }
    ]

    for cap_data in capabilities_data:
        cap = Capability(**cap_data)
        session.add(cap)

    session.commit()
    print(f"✓ Created {len(capabilities_data)} capabilities")
    session.close()


def import_employees_from_org_chart():
    """Import employees from org chart"""
    print("Importing employees from organizational chart...")

    # Create org chart
    erpnext_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    bridge = SubagentERPNextBridge(erpnext_base_url=erpnext_url)
    org_chart = ERPNextOrgChart(bridge)
    org_chart.create_complete_org_chart()

    session = db.get_session()

    # Import employees
    for emp_id, emp_data in org_chart.employee_registry.items():
        subagent_emp = emp_data["employee"]

        employee = Employee(
            employee_id=subagent_emp.employee_id,
            employee_name=subagent_emp.employee_name,
            title=emp_data["title"],
            role=subagent_emp.role,
            department=subagent_emp.department,
            subagent_type=subagent_emp.subagent_type,
            status=subagent_emp.status,
            manager_id=emp_data["manager_id"],
            created_at=datetime.fromisoformat(subagent_emp.created_at) if subagent_emp.created_at else datetime.now()
        )

        # Determine level
        if "CEO" in emp_data["title"] or "CFO" in emp_data["title"] or "CTO" in emp_data["title"] or "COO" in emp_data["title"]:
            employee.level = "C-Level"
        elif "Director" in emp_data["title"]:
            employee.level = "Director"
        elif "Lead" in emp_data["title"] or "Manager" in emp_data["title"]:
            employee.level = "Manager"
        elif "Analyst" in emp_data["title"]:
            employee.level = "Analyst"
        else:
            employee.level = "Specialist"

        session.add(employee)

    session.commit()
    print(f"✓ Imported {len(org_chart.employee_registry)} employees")
    session.close()


def import_workflows():
    """Import workflows"""
    print("Importing workflows...")

    session = db.get_session()

    all_workflows = ModuleWorkflows.get_all_workflows()
    count = 0

    for module, workflows in all_workflows.items():
        for wf in workflows:
            workflow = Workflow(
                workflow_id=wf["workflow_id"],
                workflow_name=wf["name"],
                description=f"{module} - {wf['name']}",
                department=wf["department"],
                assigned_employee_id=wf.get("assigned_to"),
                schedule_type=wf["schedule"],
                schedule_config=json.dumps({"schedule": wf["schedule"]}),
                subagent_type=wf["subagent_type"],
                task_template=wf["task"],
                is_enabled=True,
                execution_count=0
            )

            session.add(workflow)
            count += 1

    session.commit()
    print(f"✓ Imported {count} workflows")
    session.close()


def create_sample_tasks():
    """Create sample tasks for demonstration"""
    print("Creating sample tasks...")

    session = db.get_session()

    # Get some employees
    employees = session.query(Employee).limit(5).all()

    sample_tasks = [
        {
            'task_description': 'Daily lead processing - Review and qualify new leads',
            'status': 'completed',
            'progress': 100
        },
        {
            'task_description': 'Monthly sales closing - Generate invoices and reports',
            'status': 'in_progress',
            'progress': 75
        },
        {
            'task_description': 'Stock level check - Identify items below reorder point',
            'status': 'completed',
            'progress': 100
        },
        {
            'task_description': 'CRM pipeline analysis - Analyze conversion rates',
            'status': 'pending',
            'progress': 0
        }
    ]

    count = 0
    for i, task_data in enumerate(sample_tasks):
        if i < len(employees):
            emp = employees[i]
            task = Task(
                task_id=f"task_{uuid.uuid4().hex[:12]}",
                employee_id=emp.employee_id,
                employee_name=emp.employee_name,
                task_description=task_data['task_description'],
                subagent_type=emp.subagent_type,
                status=task_data['status'],
                progress=task_data['progress'],
                created_at=datetime.now()
            )

            if task_data['status'] == 'completed':
                task.completed_at = datetime.now()
                task.duration_seconds = 300

            session.add(task)
            count += 1

    session.commit()
    print(f"✓ Created {count} sample tasks")
    session.close()


def main():
    """Main initialization function"""
    print_header("DATABASE INITIALIZATION")

    print("Database URL:", os.getenv('DATABASE_URL', 'sqlite:///dogansystem.db'))
    print()

    # Create tables
    print("Step 1: Creating database tables...")
    db.create_tables()
    print("✓ Tables created\n")

    # Initialize data
    try:
        init_departments()
        init_roles()
        init_capabilities()
        import_employees_from_org_chart()
        import_workflows()
        create_sample_tasks()

        print_header("DATABASE INITIALIZATION COMPLETE")

        # Summary
        session = db.get_session()
        print("SUMMARY:")
        print("-" * 80)
        print(f"  Departments:  {session.query(Department).count()}")
        print(f"  Employees:    {session.query(Employee).count()}")
        print(f"  Roles:        {session.query(Role).count()}")
        print(f"  Capabilities: {session.query(Capability).count()}")
        print(f"  Workflows:    {session.query(Workflow).count()}")
        print(f"  Tasks:        {session.query(Task).count()}")
        print()

        print("Database file: dogansystem.db")
        print("Schema file: database_schema.sql")
        print()

        print("✓ Ready to use!")
        print("\nNext steps:")
        print("  1. View data: Use any SQLite browser")
        print("  2. Query data: Use database_query.py")
        print("  3. Dashboard: Start dashboard_api.py")

        session.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    import sys
    from database_models import Task  # Import here to avoid circular import
    sys.exit(main())
