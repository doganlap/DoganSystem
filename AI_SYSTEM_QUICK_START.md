# AI Employee Management System - Quick Start Guide

Get your AI Employee Management System (database + dashboard + orchestrator) up and running in 5 minutes!

## What You'll Get

✅ **80+ AI Employees** powered by Claude Code subagents
✅ **Complete Database** with organizational structure, roles, and workflows
✅ **40+ Automated Workflows** for ERPNext modules
✅ **Material-UI Dashboard** for management and monitoring
✅ **Full Integration** with ERPNext

## Prerequisites

- Python 3.8+
- Node.js 18+
- Git (optional)

## 5-Minute Setup

### Step 1: Set Up Environment (30 seconds)

```bash
cd DoganSystem/agent-setup

# Create .env file
cat > .env << 'EOF'
# Database (SQLite by default)
DATABASE_URL=sqlite:///dogansystem.db

# ERPNext (update with your instance)
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_api_key_here
ERPNEXT_API_SECRET=your_api_secret_here

# Claude API (required for subagents)
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
```

### Step 2: Install Dependencies (2 minutes)

```bash
# Install Python dependencies
pip install -r requirements_database.txt
pip install -r requirements_dashboard.txt

# Install Frontend dependencies
cd ../frontend
npm install
cd ../agent-setup
```

### Step 3: Initialize Database (30 seconds)

```bash
python initialize_database.py
```

**Expected output:**
```
✓ Created 13 departments
✓ Created 9 roles
✓ Created 13 capabilities
✓ Imported 80+ employees
✓ Imported 40+ workflows
✓ Created 4 sample tasks

✓ Ready to use!
```

### Step 4: Start Backend API (10 seconds)

```bash
# In terminal 1
python dashboard_api.py
```

You should see:
```
API Server: http://localhost:8007
Available endpoints:
  GET  /api/dashboard/stats
  GET  /api/employees
  GET  /api/workflows
  ...
```

### Step 5: Start Frontend (10 seconds)

```bash
# In terminal 2 (new terminal)
cd ../frontend
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Step 6: Open Dashboard (5 seconds)

Open your browser to: **http://localhost:3000**

You should see the dashboard with:
- System statistics
- Employee list
- Workflow management
- Organizational chart
- Task monitoring

## What to Do Next

### Explore the Dashboard

1. **Overview Tab**: View system statistics
2. **Employees Tab**: Browse 80+ AI employees by department
3. **Workflows Tab**: Execute automated workflows
4. **Org Chart Tab**: Visualize organizational hierarchy
5. **Tasks Tab**: Monitor active and completed tasks
6. **Analytics Tab**: View performance metrics

### Execute Your First Workflow

1. Click the **Workflows** tab
2. Find "Daily Sales Analysis" workflow
3. Click **Execute** button
4. Go to **Tasks** tab to see it running
5. View results when completed

### Query the Database

```bash
cd agent-setup

# Run query examples
python database_query.py
```

This will show:
- System statistics
- Employee list
- Department breakdown
- Active tasks

### Test the API

```bash
# Get system stats
curl http://localhost:8007/api/dashboard/stats

# Get all employees
curl http://localhost:8007/api/employees

# Get employees in Sales department
curl http://localhost:8007/api/employees?department=Sales

# Get active tasks
curl http://localhost:8007/api/tasks/active
```

## System Components

### Database (SQLite)
- **Location**: `agent-setup/dogansystem.db`
- **Tables**: 23 tables across 10 categories
- **Data**: 80+ employees, 40+ workflows, 13 departments

### Backend API (Flask)
- **Port**: 8007
- **Endpoints**: 10+ REST API endpoints
- **Integration**: Database + ERPNext + Claude Code

### Frontend (React + MUI)
- **Port**: 3000
- **Framework**: Next.js 14 + Material-UI
- **Features**: Real-time dashboard, charts, tables

## Common Tasks

### View All Employees

**Via Python:**
```python
from database_query import DatabaseQuery

query = DatabaseQuery()
employees = query.get_all_employees()

for emp in employees:
    print(f"{emp.employee_name} - {emp.title} ({emp.department})")

query.close()
```

**Via API:**
```bash
curl http://localhost:8007/api/employees | jq
```

**Via Dashboard:**
Go to Employees tab in http://localhost:3000

### Execute a Workflow

**Via Python:**
```python
from enhanced_autonomous_orchestrator import EnhancedAutonomousOrchestrator

orchestrator = EnhancedAutonomousOrchestrator()
result = orchestrator.execute_workflow('wf_sales_analysis_001')

print(f"Task ID: {result['task_details']['task_id']}")
```

**Via API:**
```bash
curl -X POST http://localhost:8007/api/workflows/wf_sales_analysis_001/execute
```

**Via Dashboard:**
Go to Workflows tab → Click Execute button

### View Organizational Hierarchy

**Via Python:**
```python
from database_query import DatabaseQuery

query = DatabaseQuery()
hierarchy = query.get_org_hierarchy('emp_ceo_001')

import json
print(json.dumps(hierarchy, indent=2))

query.close()
```

**Via Dashboard:**
Go to Org Chart tab in http://localhost:3000

## Architecture Overview

```
┌─────────────────────────────────────────┐
│  Frontend (React + MUI)                 │
│  http://localhost:3000                  │
└───────────────┬─────────────────────────┘
                │ REST API
┌───────────────▼─────────────────────────┐
│  Backend API (Flask)                    │
│  http://localhost:8007                  │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼────┐ ┌────▼────┐ ┌────▼─────┐
│Database│ │Workflows│ │Claude    │
│SQLite  │ │Engine   │ │Subagents │
└────────┘ └─────────┘ └──────────┘
```

## Configuration

### Switch to PostgreSQL

Edit `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dogansystem
```

Then re-initialize:
```bash
pip install psycopg2-binary
python initialize_database.py
```

### Update ERPNext Connection

Edit `.env`:
```env
ERPNEXT_BASE_URL=https://your-erpnext.com
ERPNEXT_API_KEY=your_actual_key
ERPNEXT_API_SECRET=your_actual_secret
```

### Configure Claude API

Edit `.env`:
```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

## Troubleshooting

### Database Not Found
```bash
cd agent-setup
python initialize_database.py
```

### API Not Responding
```bash
# Check if running
curl http://localhost:8007/api/health

# Restart if needed
python dashboard_api.py
```

### Frontend Build Error
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### No Employees Showing
```bash
# Verify database has data
python -c "from database_query import DatabaseQuery; q = DatabaseQuery(); print(f'Employees: {q.get_system_stats()[\"total_employees\"]}'); q.close()"

# Re-initialize if needed
python initialize_database.py
```

## File Locations

```
DoganSystem/
├── agent-setup/
│   ├── dogansystem.db              ← Database file (created)
│   ├── database_models.py          ← ORM models
│   ├── database_query.py           ← Query utilities
│   ├── dashboard_api.py            ← Backend API
│   ├── initialize_database.py      ← Setup script
│   └── .env                        ← Configuration (create this)
│
├── frontend/
│   ├── src/                        ← React components
│   └── package.json                ← Dependencies
│
└── Documentation/
    ├── AI_SYSTEM_QUICK_START.md    ← This file
    ├── DATABASE_COMPLETE_GUIDE.md  ← Database details
    ├── DASHBOARD_SETUP_GUIDE.md    ← Frontend details
    └── COMPLETE_SYSTEM_INTEGRATION.md  ← Architecture
```

## Documentation

- [DATABASE_COMPLETE_GUIDE.md](DATABASE_COMPLETE_GUIDE.md) - Database schema, queries, examples
- [DASHBOARD_SETUP_GUIDE.md](DASHBOARD_SETUP_GUIDE.md) - Frontend setup and components
- [COMPLETE_SYSTEM_INTEGRATION.md](COMPLETE_SYSTEM_INTEGRATION.md) - System architecture and integration

## System Statistics

After initialization, you'll have:

| Component | Count |
|-----------|-------|
| Departments | 13 |
| Employees | 80+ |
| Roles | 9 |
| Capabilities | 13 |
| Workflows | 40+ |
| Database Tables | 23 |
| API Endpoints | 10+ |
| Frontend Components | 7 |

## Next Steps

1. ✅ Explore the dashboard at http://localhost:3000
2. ✅ Execute some workflows
3. ✅ Query the database
4. ✅ Read the detailed documentation
5. ✅ Connect to your actual ERPNext instance
6. ✅ Customize workflows for your needs

---

**Your AI Employee Management System is Ready!** 🚀

Go to **http://localhost:3000** to start managing your AI workforce.
