# Complete Database System - Guide

## Overview

A comprehensive **SQLite/PostgreSQL database system** with complete schema for employees, organizational structure, roles, responsibilities, scopes, workflows, tasks, and analytics.

## Database Architecture

### 📊 **10 Main Categories** with 23 Tables:

1. **Employees & Organization** (3 tables)
   - employees, departments, teams

2. **Roles & Responsibilities** (3 tables)
   - roles, responsibilities, employee_roles

3. **Capabilities & Scope** (3 tables)
   - capabilities, employee_capabilities, scopes

4. **Organizational Structure** (2 tables)
   - team_members, (departments/teams covered above)

5. **Workflows & Tasks** (3 tables)
   - workflows, tasks, task_dependencies

6. **Performance & Analytics** (2 tables)
   - employee_metrics, department_metrics

7. **ERPNext Integration** (2 tables)
   - erpnext_access, erpnext_actions

8. **Audit & Logging** (2 tables)
   - audit_log, system_events

9. **Configuration** (1 table)
   - system_config

10. **Notifications** (1 table)
    - notifications

### 📈 **3 Views** for Common Queries:
- v_employee_details
- v_employee_task_stats
- v_department_summary

## Quick Setup

### Step 1: Install Dependencies

```bash
cd agent-setup
pip install -r requirements_database.txt
```

### Step 2: Initialize Database

```bash
python initialize_database.py
```

**Output:**
```
================================================================================
                       DATABASE INITIALIZATION
================================================================================

Database URL: sqlite:///dogansystem.db

Step 1: Creating database tables...
✓ Tables created

Creating departments...
✓ Created 13 departments

Creating roles and responsibilities...
✓ Created 9 roles

Creating capabilities...
✓ Created 13 capabilities

Importing employees from organizational chart...
✓ Imported 80+ employees

Importing workflows...
✓ Imported 40+ workflows

Creating sample tasks...
✓ Created 4 sample tasks

================================================================================
                   DATABASE INITIALIZATION COMPLETE
================================================================================

SUMMARY:
--------------------------------------------------------------------------------
  Departments:  13
  Employees:    80+
  Roles:        9
  Capabilities: 13
  Workflows:    40+
  Tasks:        4

Database file: dogansystem.db
Schema file: database_schema.sql

✓ Ready to use!
```

### Step 3: Query Database

```bash
python database_query.py
```

## Database Schema

### 1. Employees Table

```sql
CREATE TABLE employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    employee_name VARCHAR(200) NOT NULL,
    employee_name_en VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),

    title VARCHAR(200) NOT NULL,
    role VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    level VARCHAR(50), -- C-Level, Director, Manager, Specialist

    subagent_type VARCHAR(50) NOT NULL, -- Explore, Plan, general-purpose
    status VARCHAR(50) DEFAULT 'available',

    manager_id VARCHAR(50),
    team_id VARCHAR(50),

    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    last_active TIMESTAMP
);
```

### 2. Departments Table

```sql
CREATE TABLE departments (
    department_id VARCHAR(50) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_name_ar VARCHAR(100),
    description TEXT,
    erpnext_module VARCHAR(100),

    parent_department_id VARCHAR(50),
    head_employee_id VARCHAR(50),

    email VARCHAR(200),
    phone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 3. Roles Table

```sql
CREATE TABLE roles (
    role_id VARCHAR(50) PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    role_description TEXT,
    level VARCHAR(50),
    department VARCHAR(100),

    can_approve_workflows BOOLEAN DEFAULT FALSE,
    can_manage_employees BOOLEAN DEFAULT FALSE,
    can_execute_tasks BOOLEAN DEFAULT FALSE,
    can_view_analytics BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 4. Responsibilities Table

```sql
CREATE TABLE responsibilities (
    responsibility_id VARCHAR(50) PRIMARY KEY,
    role_id VARCHAR(50) NOT NULL,

    responsibility_name VARCHAR(200) NOT NULL,
    responsibility_description TEXT,
    scope TEXT,
    priority INTEGER DEFAULT 0,

    category VARCHAR(100), -- Strategic, Operational, Administrative
    frequency VARCHAR(50), -- Daily, Weekly, Monthly, As-needed

    created_at TIMESTAMP
);
```

### 5. Capabilities Table

```sql
CREATE TABLE capabilities (
    capability_id VARCHAR(50) PRIMARY KEY,
    capability_name VARCHAR(200) NOT NULL UNIQUE,
    capability_description TEXT,

    category VARCHAR(100), -- Technical, Business, Analytical
    skill_level VARCHAR(50), -- Basic, Intermediate, Advanced, Expert

    erpnext_module VARCHAR(100),
    erpnext_doctype VARCHAR(100),

    created_at TIMESTAMP
);
```

### 6. Scopes Table

```sql
CREATE TABLE scopes (
    scope_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,

    scope_name VARCHAR(200) NOT NULL,
    scope_description TEXT,
    scope_type VARCHAR(50), -- Geographic, Functional, Product

    erpnext_modules TEXT, -- JSON array
    customer_segments TEXT, -- JSON array
    geographical_areas TEXT, -- JSON array

    budget_limit DECIMAL(15,2),
    approval_required BOOLEAN DEFAULT FALSE,

    effective_from DATE,
    effective_to DATE,

    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 7. Workflows Table

```sql
CREATE TABLE workflows (
    workflow_id VARCHAR(50) PRIMARY KEY,
    workflow_name VARCHAR(200) NOT NULL,
    description TEXT,

    department VARCHAR(100),
    assigned_employee_id VARCHAR(50),

    schedule_type VARCHAR(50),
    schedule_config TEXT, -- JSON

    subagent_type VARCHAR(50) NOT NULL,
    task_template TEXT NOT NULL,

    is_enabled BOOLEAN DEFAULT TRUE,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    execution_count INTEGER DEFAULT 0,

    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 8. Tasks Table

```sql
CREATE TABLE tasks (
    task_id VARCHAR(50) PRIMARY KEY,
    workflow_id VARCHAR(50),
    employee_id VARCHAR(50) NOT NULL,
    employee_name VARCHAR(200),

    task_description TEXT NOT NULL,
    subagent_type VARCHAR(50) NOT NULL,

    status VARCHAR(50) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,

    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    result TEXT, -- JSON
    error_message TEXT,

    priority INTEGER DEFAULT 0,
    tags TEXT -- JSON
);
```

## Using the Database

### Python ORM (SQLAlchemy)

```python
from database_models import db, Employee, Department, Task
from database_query import DatabaseQuery

# Get session
session = db.get_session()

# Query employees
employees = session.query(Employee)\
    .filter_by(department='Sales')\
    .filter_by(status='available')\
    .all()

for emp in employees:
    print(f"{emp.employee_name} - {emp.title}")

# Using query helper
query = DatabaseQuery()
stats = query.get_system_stats()
print(stats)
query.close()
```

### Direct SQL Queries

```bash
# Open database
sqlite3 dogansystem.db

# Query employees
SELECT employee_name, title, department, status
FROM employees
WHERE department = 'Sales';

# Get department summary
SELECT * FROM v_department_summary;

# Get employee task stats
SELECT * FROM v_employee_task_stats
WHERE total_tasks > 0
ORDER BY completed_tasks DESC;
```

## Common Queries

### 1. Get All Employees in a Department

```python
from database_query import DatabaseQuery

query = DatabaseQuery()
sales_employees = query.get_all_employees(department='Sales')

for emp in sales_employees:
    print(f"{emp.employee_name} - {emp.title}")

query.close()
```

### 2. Get Employee with Statistics

```python
query = DatabaseQuery()
stats = query.get_employee_stats('emp_sales_dir_001')

print(f"Total Tasks: {stats['total_tasks']}")
print(f"Completed: {stats['completed_tasks']}")
print(f"Success Rate: {stats['success_rate']}%")

query.close()
```

### 3. Get Active Tasks

```python
query = DatabaseQuery()
active_tasks = query.get_active_tasks()

for task in active_tasks:
    print(f"{task.task_id}: {task.task_description[:50]}...")
    print(f"  Employee: {task.employee_name}")
    print(f"  Status: {task.status}")

query.close()
```

### 4. Search Employees

```python
query = DatabaseQuery()
results = query.search_employees("Mohammed")

for emp in results:
    print(f"{emp.employee_name} - {emp.department}")

query.close()
```

### 5. Get Organizational Hierarchy

```python
query = DatabaseQuery()
hierarchy = query.get_org_hierarchy('emp_ceo_001')

import json
print(json.dumps(hierarchy, indent=2))

query.close()
```

## Database Views

### v_employee_details

```sql
SELECT
    e.employee_id,
    e.employee_name,
    e.title,
    e.department,
    m.employee_name as manager_name,
    t.team_name,
    d.department_name,
    COUNT(DISTINCT ec.capability_id) as total_capabilities,
    COUNT(DISTINCT er.role_id) as total_roles
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
LEFT JOIN teams t ON e.team_id = t.team_id
LEFT JOIN departments d ON e.department = d.department_id
GROUP BY e.employee_id;
```

**Usage:**
```sql
SELECT * FROM v_employee_details
WHERE department = 'Sales';
```

### v_employee_task_stats

```sql
SELECT
    e.employee_id,
    e.employee_name,
    COUNT(t.task_id) as total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN t.status = 'failed' THEN 1 ELSE 0 END) as failed_tasks,
    AVG(CASE WHEN t.status = 'completed' THEN t.duration_seconds END) as avg_duration
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
GROUP BY e.employee_id;
```

**Usage:**
```sql
SELECT * FROM v_employee_task_stats
ORDER BY total_tasks DESC
LIMIT 10;
```

## Data Migration

### Export to JSON

```python
from database_query import DatabaseQuery
import json

query = DatabaseQuery()

# Export all employees
employees = query.get_all_employees()
data = [emp.to_dict() for emp in employees]

with open('employees_export.json', 'w') as f:
    json.dump(data, f, indent=2)

query.close()
```

### Import from JSON

```python
from database_models import db, Employee
import json

with open('employees_export.json', 'r') as f:
    data = json.load(f)

session = db.get_session()

for emp_data in data:
    emp = Employee(**emp_data)
    session.add(emp)

session.commit()
session.close()
```

## Backup & Restore

### Backup SQLite Database

```bash
# Backup
sqlite3 dogansystem.db ".backup dogansystem_backup.db"

# Or copy file
cp dogansystem.db dogansystem_backup_$(date +%Y%m%d).db
```

### Export to SQL

```bash
sqlite3 dogansystem.db .dump > dogansystem_dump.sql
```

### Restore from SQL

```bash
sqlite3 dogansystem_new.db < dogansystem_dump.sql
```

## Switching to PostgreSQL

### 1. Update Environment

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dogansystem
```

### 2. Install PostgreSQL Driver

```bash
pip install psycopg2-binary
```

### 3. Run Initialization

```bash
python initialize_database.py
```

The system automatically detects PostgreSQL from the connection string!

## Performance Optimization

### Create Indexes

Already included in schema:
```sql
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_tasks_employee ON tasks(employee_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

### Query Optimization

```python
# BAD: N+1 queries
for emp in session.query(Employee).all():
    print(emp.manager.name)  # Separate query each time

# GOOD: Eager loading
from sqlalchemy.orm import joinedload

employees = session.query(Employee)\
    .options(joinedload(Employee.manager))\
    .all()

for emp in employees:
    print(emp.manager.name if emp.manager else "No manager")
```

## Files Created

```
agent-setup/
├── database_schema.sql              ✅ (900+ lines) - Complete SQL schema
├── database_models.py               ✅ (600+ lines) - SQLAlchemy models
├── initialize_database.py           ✅ (400+ lines) - Database setup script
├── database_query.py                ✅ (300+ lines) - Query utilities
└── requirements_database.txt        ✅ - Dependencies

root/
└── DATABASE_COMPLETE_GUIDE.md       ✅ - This guide
```

## Next Steps

1. ✅ Run initialization: `python initialize_database.py`
2. ✅ Query database: `python database_query.py`
3. ✅ Browse with SQLite viewer
4. ✅ Integrate with dashboard API
5. ✅ Add custom queries as needed

---

**Your complete database system is ready!** 📊✨
