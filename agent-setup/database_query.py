"""
Database Query Utility
Convenient functions to query the database
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from database_models import (
    db, Employee, Department, Team, Role, Capability,
    Workflow, Task, EmployeeMetrics
)


class DatabaseQuery:
    """Database query helper class"""

    def __init__(self):
        self.session = db.get_session()

    def close(self):
        """Close session"""
        self.session.close()

    # ===== EMPLOYEE QUERIES =====

    def get_all_employees(self, department: str = None, status: str = None):
        """Get all employees with optional filters"""
        query = self.session.query(Employee)

        if department:
            query = query.filter(Employee.department == department)
        if status:
            query = query.filter(Employee.status == status)

        return query.all()

    def get_employee(self, employee_id: str):
        """Get single employee"""
        return self.session.query(Employee).filter_by(employee_id=employee_id).first()

    def get_employees_by_manager(self, manager_id: str):
        """Get all employees under a manager"""
        return self.session.query(Employee).filter_by(manager_id=manager_id).all()

    def get_available_employees(self, subagent_type: str = None):
        """Get available employees"""
        query = self.session.query(Employee).filter_by(status='available')

        if subagent_type:
            query = query.filter_by(subagent_type=subagent_type)

        return query.all()

    # ===== DEPARTMENT QUERIES =====

    def get_all_departments(self):
        """Get all departments"""
        return self.session.query(Department).filter_by(is_active=True).all()

    def get_department_with_stats(self, department_id: str):
        """Get department with employee count"""
        dept = self.session.query(Department).filter_by(department_id=department_id).first()

        if dept:
            employee_count = self.session.query(func.count(Employee.employee_id))\
                .filter_by(department=department_id).scalar()

            workflow_count = self.session.query(func.count(Workflow.workflow_id))\
                .filter_by(department=department_id).scalar()

            return {
                'department': dept,
                'employee_count': employee_count,
                'workflow_count': workflow_count
            }

        return None

    # ===== WORKFLOW QUERIES =====

    def get_all_workflows(self, enabled_only: bool = True):
        """Get all workflows"""
        query = self.session.query(Workflow)

        if enabled_only:
            query = query.filter_by(is_enabled=True)

        return query.all()

    def get_workflows_by_department(self, department: str):
        """Get workflows for a department"""
        return self.session.query(Workflow).filter_by(department=department).all()

    def get_due_workflows(self):
        """Get workflows that are due to run"""
        now = datetime.now()
        return self.session.query(Workflow)\
            .filter(Workflow.is_enabled == True)\
            .filter(Workflow.next_run <= now)\
            .all()

    # ===== TASK QUERIES =====

    def get_tasks(
        self,
        employee_id: str = None,
        workflow_id: str = None,
        status: str = None,
        limit: int = 50
    ):
        """Get tasks with filters"""
        query = self.session.query(Task).order_by(desc(Task.created_at))

        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if workflow_id:
            query = query.filter_by(workflow_id=workflow_id)
        if status:
            query = query.filter_by(status=status)

        return query.limit(limit).all()

    def get_active_tasks(self):
        """Get currently active tasks"""
        return self.session.query(Task)\
            .filter(Task.status.in_(['pending', 'in_progress']))\
            .order_by(desc(Task.created_at))\
            .all()

    def get_completed_tasks_today(self):
        """Get tasks completed today"""
        today = datetime.now().date()
        return self.session.query(Task)\
            .filter_by(status='completed')\
            .filter(func.date(Task.completed_at) == today)\
            .all()

    # ===== STATISTICS =====

    def get_employee_stats(self, employee_id: str):
        """Get statistics for an employee"""
        total_tasks = self.session.query(func.count(Task.task_id))\
            .filter_by(employee_id=employee_id).scalar()

        completed = self.session.query(func.count(Task.task_id))\
            .filter_by(employee_id=employee_id, status='completed').scalar()

        failed = self.session.query(func.count(Task.task_id))\
            .filter_by(employee_id=employee_id, status='failed').scalar()

        avg_duration = self.session.query(func.avg(Task.duration_seconds))\
            .filter_by(employee_id=employee_id, status='completed').scalar()

        return {
            'total_tasks': total_tasks or 0,
            'completed_tasks': completed or 0,
            'failed_tasks': failed or 0,
            'success_rate': (completed / total_tasks * 100) if total_tasks > 0 else 0,
            'avg_duration_seconds': int(avg_duration) if avg_duration else 0
        }

    def get_department_stats(self, department: str):
        """Get statistics for a department"""
        employees = self.session.query(Employee).filter_by(department=department).all()
        employee_ids = [e.employee_id for e in employees]

        total_tasks = self.session.query(func.count(Task.task_id))\
            .filter(Task.employee_id.in_(employee_ids)).scalar()

        completed = self.session.query(func.count(Task.task_id))\
            .filter(Task.employee_id.in_(employee_ids), Task.status == 'completed').scalar()

        return {
            'total_employees': len(employees),
            'total_tasks': total_tasks or 0,
            'completed_tasks': completed or 0
        }

    def get_system_stats(self):
        """Get overall system statistics"""
        return {
            'total_employees': self.session.query(func.count(Employee.employee_id)).scalar(),
            'available_employees': self.session.query(func.count(Employee.employee_id))\
                .filter_by(status='available').scalar(),
            'total_departments': self.session.query(func.count(Department.department_id))\
                .filter_by(is_active=True).scalar(),
            'total_workflows': self.session.query(func.count(Workflow.workflow_id)).scalar(),
            'enabled_workflows': self.session.query(func.count(Workflow.workflow_id))\
                .filter_by(is_enabled=True).scalar(),
            'total_tasks': self.session.query(func.count(Task.task_id)).scalar(),
            'completed_tasks': self.session.query(func.count(Task.task_id))\
                .filter_by(status='completed').scalar(),
            'active_tasks': self.session.query(func.count(Task.task_id))\
                .filter(Task.status.in_(['pending', 'in_progress'])).scalar()
        }

    # ===== SEARCH =====

    def search_employees(self, search_term: str):
        """Search employees by name"""
        search = f"%{search_term}%"
        return self.session.query(Employee)\
            .filter(
                (Employee.employee_name.like(search)) |
                (Employee.employee_name_en.like(search)) |
                (Employee.title.like(search))
            )\
            .all()

    # ===== ORGANIZATIONAL HIERARCHY =====

    def get_org_hierarchy(self, root_employee_id: str = 'emp_ceo_001'):
        """Get organizational hierarchy starting from root"""
        def build_tree(employee_id):
            employee = self.get_employee(employee_id)
            if not employee:
                return None

            reports = self.get_employees_by_manager(employee_id)

            return {
                'employee_id': employee.employee_id,
                'name': employee.employee_name,
                'title': employee.title,
                'department': employee.department,
                'reports': [build_tree(r.employee_id) for r in reports]
            }

        return build_tree(root_employee_id)


# Example usage and testing
if __name__ == "__main__":
    import json

    print("\n" + "="*80)
    print("DATABASE QUERY EXAMPLES")
    print("="*80 + "\n")

    query = DatabaseQuery()

    # System stats
    print("SYSTEM STATISTICS:")
    print("-" * 80)
    stats = query.get_system_stats()
    print(json.dumps(stats, indent=2))

    # List employees
    print("\n\nEMPLOYEES:")
    print("-" * 80)
    employees = query.get_all_employees()
    for emp in employees[:10]:  # First 10
        print(f"  {emp.employee_name:30} | {emp.title:30} | {emp.department}")

    # Department stats
    print("\n\nDEPARTMENT STATISTICS:")
    print("-" * 80)
    for dept in query.get_all_departments():
        dept_stats = query.get_department_stats(dept.department_id)
        print(f"  {dept.department_name:20} | Employees: {dept_stats['total_employees']:3} | Tasks: {dept_stats['total_tasks']:4}")

    # Active tasks
    print("\n\nACTIVE TASKS:")
    print("-" * 80)
    active = query.get_active_tasks()
    for task in active[:5]:  # First 5
        print(f"  {task.task_id} | {task.employee_name:25} | {task.status}")

    query.close()

    print("\n" + "="*80)
