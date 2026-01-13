"""
Dashboard API Server
Provides REST API for the MUI dashboard frontend
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Import our modules
from claude_code_bridge import SubagentERPNextBridge
from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator
from erpnext_org_chart import ERPNextOrgChart
from org_chart_workflows import ModuleWorkflows
from database_query import DatabaseQuery
from database_models import db, Employee, Department, Workflow, Task
from claude_ai_service import register_claude_routes, claude_service

# Load environment
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
erpnext_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
bridge = SubagentERPNextBridge(erpnext_base_url=erpnext_url)
orchestrator = EnhancedAutonomousOrchestrator(erpnext_base_url=erpnext_url)
org_chart = None  # Lazy load


def get_org_chart():
    """Get or create org chart"""
    global org_chart
    if org_chart is None:
        org_chart = ERPNextOrgChart(bridge)
        org_chart.create_complete_org_chart()
    return org_chart


def get_db_query():
    """Get database query instance"""
    return DatabaseQuery()


# ===== Dashboard API Endpoints =====

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    query = None
    try:
        query = get_db_query()
        stats = query.get_system_stats()

        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get list of all employees"""
    query = None
    try:
        department = request.args.get('department')
        status = request.args.get('status')

        query = get_db_query()
        employees = query.get_all_employees(department=department, status=status)

        result = []
        for emp in employees:
            result.append({
                "id": emp.employee_id,
                "name": emp.employee_name,
                "title": emp.title,
                "role": emp.role,
                "department": emp.department,
                "type": emp.subagent_type,
                "status": emp.status,
                "level": emp.level,
                "created_at": emp.created_at.isoformat() if emp.created_at else None,
            })

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting employees: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get single employee details"""
    query = None
    try:
        query = get_db_query()
        employee = query.get_employee(employee_id)

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # Get task history and stats for this employee
        tasks = query.get_tasks(employee_id=employee_id, limit=10)
        stats = query.get_employee_stats(employee_id)

        result = {
            "id": employee.employee_id,
            "name": employee.employee_name,
            "title": employee.title,
            "role": employee.role,
            "department": employee.department,
            "type": employee.subagent_type,
            "status": employee.status,
            "level": employee.level,
            "created_at": employee.created_at.isoformat() if employee.created_at else None,
            "stats": stats,
            "task_history": [
                {
                    "task_id": t.task_id,
                    "description": t.task_description[:100],
                    "status": t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    "completed_at": t.completed_at.isoformat() if t.completed_at else None,
                }
                for t in tasks
            ],
        }

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting employee {employee_id}: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Get list of all workflows"""
    query = None
    try:
        query = get_db_query()
        workflows = query.get_all_workflows(enabled_only=False)

        result = []
        for wf in workflows:
            result.append({
                "id": wf.workflow_id,
                "name": wf.workflow_name,
                "description": wf.description,
                "department": wf.department,
                "schedule_type": wf.schedule_type,
                "subagent_type": wf.subagent_type,
                "enabled": wf.is_enabled,
                "last_run": wf.last_run.isoformat() if wf.last_run else None,
                "next_run": wf.next_run.isoformat() if wf.next_run else None,
                "execution_count": wf.execution_count,
            })

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting workflows: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute a workflow manually"""
    try:
        result = orchestrator.execute_workflow(workflow_id)
        return jsonify({
            "success": True,
            "workflow_id": result["workflow_id"],
            "workflow_name": result["workflow_name"],
            "execution_time": result["execution_time"],
            "task_id": result["task_details"]["task_id"],
        })
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get task history"""
    query = None
    try:
        employee_id = request.args.get('employee_id')
        status = request.args.get('status')
        limit = int(request.args.get('limit', 50))

        query = get_db_query()
        tasks = query.get_tasks(employee_id=employee_id, status=status, limit=limit)

        result = []
        for task in tasks:
            result.append({
                "task_id": task.task_id,
                "employee_id": task.employee_id,
                "employee_name": task.employee_name,
                "description": task.task_description[:200],
                "status": task.status,
                "subagent_type": task.subagent_type,
                "progress": task.progress,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "duration_seconds": task.duration_seconds,
                "error": task.error_message,
            })

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/tasks/active', methods=['GET'])
def get_active_tasks():
    """Get currently active/pending tasks"""
    query = None
    try:
        query = get_db_query()
        tasks = query.get_active_tasks()

        result = []
        for task in tasks:
            employee = query.get_employee(task.employee_id)
            result.append({
                "task_id": task.task_id,
                "name": task.task_description[:100],
                "employee_id": task.employee_id,
                "employee_name": task.employee_name,
                "department": employee.department if employee else "Unknown",
                "status": task.status,
                "started_at": task.created_at.isoformat() if task.created_at else None,
                "progress": task.progress or (50 if task.status == "in_progress" else 0),
            })

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting active tasks: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/org-chart', methods=['GET'])
def get_org_chart_data():
    """Get organizational chart data"""
    query = None
    try:
        query = get_db_query()

        # Get organizational hierarchy from database
        hierarchy = query.get_org_hierarchy('emp_ceo_001')

        # Get summary stats
        stats = query.get_system_stats()
        dept_summary = {}
        for dept in query.get_all_departments():
            dept_stats = query.get_department_stats(dept.department_id)
            dept_summary[dept.department_name] = dept_stats['total_employees']

        return jsonify({
            "hierarchy": hierarchy,
            "summary": {
                "total_employees": stats['total_employees'],
                "by_department": dept_summary,
            },
        })
    except Exception as e:
        logger.error(f"Error getting org chart: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/departments', methods=['GET'])
def get_departments():
    """Get department statistics"""
    query = None
    try:
        query = get_db_query()
        departments = []

        for dept in query.get_all_departments():
            dept_stats = query.get_department_stats(dept.department_id)
            departments.append({
                "id": dept.department_id,
                "name": dept.department_name,
                "name_ar": dept.department_name_ar,
                "description": dept.description,
                "employee_count": dept_stats['total_employees'],
                "total_tasks": dept_stats['total_tasks'],
                "completed_tasks": dept_stats['completed_tasks'],
            })

        return jsonify(departments)
    except Exception as e:
        logger.error(f"Error getting departments: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/api/analytics/performance', methods=['GET'])
def get_performance_analytics():
    """Get performance analytics"""
    query = None
    try:
        query = get_db_query()
        stats = query.get_system_stats()

        # Calculate metrics
        total_tasks = stats['total_tasks']
        completed = stats['completed_tasks']
        failed_count = total_tasks - completed - stats['active_tasks']
        success_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0

        # By department
        dept_stats = {}
        for dept in query.get_all_departments():
            dept_data = query.get_department_stats(dept.department_id)
            dept_stats[dept.department_name] = {
                "total": dept_data['total_tasks'],
                "completed": dept_data['completed_tasks'],
                "success_rate": (dept_data['completed_tasks'] / dept_data['total_tasks'] * 100)
                    if dept_data['total_tasks'] > 0 else 0
            }

        return jsonify({
            "total_tasks": total_tasks,
            "completed_tasks": completed,
            "failed_tasks": failed_count,
            "success_rate": round(success_rate, 2),
            "by_department": dept_stats,
        })
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if query:
            query.close()


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - API info"""
    return jsonify({
        "name": "DoganSystem Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "stats": "/api/dashboard/stats",
            "employees": "/api/employees",
            "workflows": "/api/workflows",
            "tasks": "/api/tasks",
            "org_chart": "/api/org-chart",
            "departments": "/api/departments",
            "analytics": "/api/analytics/performance",
            "health": "/api/health"
        },
        "docs": "Access any endpoint to get data"
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "erpnext_url": erpnext_url,
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# Register Claude AI routes
register_claude_routes(app)


if __name__ == '__main__':
    print("\n" + "="*80)
    print("DASHBOARD API SERVER")
    print("="*80)
    print(f"\nERPNext URL: {erpnext_url}")
    print("API Server: http://localhost:8007")
    print("\nAvailable endpoints:")
    print("  GET  /api/dashboard/stats")
    print("  GET  /api/employees")
    print("  GET  /api/workflows")
    print("  POST /api/workflows/<id>/execute")
    print("  GET  /api/tasks")
    print("  GET  /api/tasks/active")
    print("  GET  /api/org-chart")
    print("  GET  /api/departments")
    print("  GET  /api/analytics/performance")
    print("\nClaude AI endpoints:")
    print("  POST /api/ai/chat")
    print("  POST /api/ai/analyze")
    print("  GET  /api/ai/status")
    print(f"\nClaude AI: {'Configured' if claude_service.is_configured() else 'Not configured (set ANTHROPIC_API_KEY)'}")
    print("\n" + "="*80)
    print("\nStarting server...\n")

    app.run(host='0.0.0.0', port=8007, debug=True)
