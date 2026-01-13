# Material-UI Dashboard Setup Guide

## Overview

A beautiful, modern web dashboard built with Material-UI (MUI) to manage your 80+ AI employees, workflows, and organizational structure.

## Features

✨ **Dashboard Features:**
- 📊 Real-time statistics and monitoring
- 👥 Employee management with filters and search
- 🔄 Workflow execution and monitoring
- 🏢 Interactive organizational chart
- 📈 Task monitoring with progress tracking
- 🎨 Beautiful Material-UI components
- 📱 Fully responsive design

## Architecture

```
Frontend (React + MUI)  ←→  API Server (Flask)  ←→  AI Employees (Python)
   Port 5173                  Port 8007                ERPNext Integration
```

## Quick Setup (5 Minutes)

### Step 1: Install Backend Dependencies

```bash
cd agent-setup

# Install dashboard API requirements
pip install -r requirements_dashboard.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd ../frontend

# Install Node.js dependencies
npm install
```

### Step 3: Start the API Server

```bash
# In agent-setup directory
cd ../agent-setup
python dashboard_api.py
```

**Output:**
```
DASHBOARD API SERVER
================================================================================
ERPNext URL: http://localhost:8000
API Server: http://localhost:8007

Available endpoints:
  GET  /api/dashboard/stats
  GET  /api/employees
  GET  /api/workflows
  ...

Starting server...
```

### Step 4: Start the Frontend

```bash
# In frontend directory (new terminal)
cd ../frontend
npm run dev
```

**Output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 5: Open Dashboard

Open your browser and navigate to:
```
http://localhost:5173
```

## Dashboard Pages

### 1. Overview Dashboard
- **Total employees**: 80+
- **Active workflows**: 42
- **Tasks completed**: Real-time counter
- **Department breakdown**: Visual charts
- **Recent activity**: Latest task completions

### 2. Employees Page
**Features:**
- Search employees by name
- Filter by department
- Filter by type (Explore/Plan/Operations)
- View employee details
- See task history
- Check current status (Available/Busy)

**Employee Information:**
- Name (Arabic & English)
- Title and role
- Department
- Subagent type
- Tasks completed
- Current status

### 3. Workflows Page
**Features:**
- View all 40+ workflows
- Execute workflows manually
- See schedule information
- Check last run time
- View execution count
- Enable/disable workflows

**Workflow Information:**
- Workflow name
- Department
- Schedule (hourly/daily/weekly/monthly)
- Assigned employee
- Status and statistics

### 4. Organization Chart
**Features:**
- Interactive hierarchical view
- Zoom in/out controls
- 4 organizational levels
- Department visualization
- Employee count per level

**Hierarchy:**
```
CEO
├── CTO → IT Director
├── CFO → Finance & Assets Directors
└── COO → All operational directors
```

### 5. Task Monitor
**Features:**
- Active tasks with progress bars
- Completed tasks history
- Failed tasks with error details
- Real-time status updates
- Task duration tracking

## API Endpoints

### Dashboard Statistics
```bash
GET http://localhost:8007/api/dashboard/stats

Response:
{
  "total_employees": 80,
  "available_employees": 75,
  "busy_employees": 5,
  "total_departments": 13,
  "total_workflows": 42,
  "total_tasks": 1247,
  "completed_tasks": 1180,
  "failed_tasks": 12,
  "pending_tasks": 5
}
```

### Get Employees
```bash
GET http://localhost:8007/api/employees
GET http://localhost:8007/api/employees?department=Sales
GET http://localhost:8007/api/employees?type=Explore

Response:
[
  {
    "id": "emp_sales_dir_001",
    "name": "محمد المبيعات",
    "role": "Sales Director",
    "department": "Sales",
    "type": "Plan",
    "status": "available",
    "capabilities": [...]
  }
]
```

### Get Workflows
```bash
GET http://localhost:8007/api/workflows

Response:
[
  {
    "id": "crm_lead_processing",
    "name": "Daily Lead Processing",
    "schedule": "daily_9am",
    "enabled": true,
    "last_run": "2024-01-04T09:00:00",
    "execution_count": 145
  }
]
```

### Execute Workflow
```bash
POST http://localhost:8007/api/workflows/crm_lead_processing/execute

Response:
{
  "success": true,
  "workflow_id": "crm_lead_processing",
  "task_id": "task_20240104_100000_1"
}
```

### Get Active Tasks
```bash
GET http://localhost:8007/api/tasks/active

Response:
[
  {
    "task_id": "task_001",
    "name": "Processing monthly sales closing",
    "employee_name": "Mohammed Al-Mabiyat",
    "department": "Sales",
    "status": "in_progress",
    "progress": 75
  }
]
```

### Get Org Chart
```bash
GET http://localhost:8007/api/org-chart

Response:
{
  "hierarchy": {
    "id": "emp_ceo_001",
    "name": "Abdullah Al-Muhandis",
    "title": "CEO",
    "children": [...]
  },
  "summary": {
    "total_employees": 80,
    "by_department": {...}
  }
}
```

## Customization

### Change Theme Colors

Edit `frontend/src/theme.ts`:
```typescript
const theme = createTheme({
  palette: {
    primary: {
      main: '#667eea',  // Change to your color
    },
    secondary: {
      main: '#764ba2',  // Change to your color
    },
  },
})
```

### Add New Dashboard Tab

1. Create component in `frontend/src/components/`
2. Import in `frontend/src/app/page.tsx`
3. Add to tabs array
4. Create TabPanel

### Add New API Endpoint

Edit `agent-setup/dashboard_api.py`:
```python
@app.route('/api/my-endpoint', methods=['GET'])
def my_endpoint():
    return jsonify({"data": "your data"})
```

## Development

### Frontend Development

```bash
cd frontend

# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Development

```bash
cd agent-setup

# Run with debug mode
python dashboard_api.py

# The server will reload on code changes
```

## Production Deployment

### Step 1: Build Frontend

```bash
cd frontend
npm run build
```

This creates `frontend/dist/` with optimized files.

### Step 2: Serve with Nginx

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api {
        proxy_pass http://localhost:8007;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 3: Run API with Gunicorn

```bash
cd agent-setup

# Install gunicorn
pip install gunicorn

# Run API server
gunicorn -w 4 -b 0.0.0.0:8007 dashboard_api:app
```

### Step 4: Use Process Manager

**Using PM2:**
```bash
# Install PM2
npm install -g pm2

# Start API server
pm2 start "gunicorn -w 4 -b 0.0.0.0:8007 dashboard_api:app" --name dashboard-api

# Save configuration
pm2 save
pm2 startup
```

**Using systemd:**

Create `/etc/systemd/system/dashboard-api.service`:
```ini
[Unit]
Description=Dashboard API Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/agent-setup
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:8007 dashboard_api:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable dashboard-api
sudo systemctl start dashboard-api
```

## Troubleshooting

### Issue: Frontend not connecting to API

**Solution:**
1. Check API is running: `curl http://localhost:8007/api/health`
2. Verify CORS is enabled in `dashboard_api.py`
3. Check frontend proxy in `next.config.js` (if using Next.js) or vite config

### Issue: Employee data not loading

**Solution:**
1. Create organization first: `python create_complete_organization.py`
2. Check API endpoint: `curl http://localhost:8007/api/employees`
3. Verify bridge initialization in `dashboard_api.py`

### Issue: Port already in use

**Solution:**
```bash
# Find process using port 8007
lsof -i :8007   # Mac/Linux
netstat -ano | findstr :8007  # Windows

# Kill the process or use different port
```

### Issue: Build errors

**Solution:**
```bash
cd frontend

# Clear cache
rm -rf node_modules
rm package-lock.json

# Reinstall
npm install

# Try build again
npm run build
```

## File Structure

```
DoganSystem/
├── frontend/                       # React + MUI Dashboard
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx         # Main layout
│   │   │   └── page.tsx           # Home page
│   │   ├── components/
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── StatsCard.tsx
│   │   │   ├── EmployeeList.tsx
│   │   │   ├── WorkflowList.tsx
│   │   │   ├── OrgChartView.tsx
│   │   │   └── TaskMonitor.tsx
│   │   └── theme.ts               # MUI theme
│   ├── package.json
│   └── tsconfig.json
│
└── agent-setup/                    # Backend API
    ├── dashboard_api.py           # Flask API server
    ├── requirements_dashboard.txt
    ├── claude_code_bridge.py
    ├── erpnext_org_chart.py
    └── enhanced_autonomous_orchestrator.py
```

## Features Showcase

### Beautiful UI Components

- ✅ Material-UI design system
- ✅ Responsive grid layout
- ✅ Data tables with sorting/filtering
- ✅ Progress indicators
- ✅ Status chips and badges
- ✅ Interactive charts
- ✅ Drawer navigation
- ✅ Modal dialogs

### Real-time Updates

- ✅ Live task monitoring
- ✅ Employee status tracking
- ✅ Workflow execution status
- ✅ Activity feed
- ✅ Statistics dashboard

### User Experience

- ✅ Smooth transitions
- ✅ Loading states
- ✅ Error handling
- ✅ Search and filters
- ✅ Pagination
- ✅ Toast notifications
- ✅ Mobile responsive

## Next Steps

1. ✅ Start backend: `python dashboard_api.py`
2. ✅ Start frontend: `npm run dev`
3. ✅ Open dashboard: `http://localhost:5173`
4. ✅ Explore employees, workflows, and org chart
5. ✅ Execute workflows manually
6. ✅ Monitor tasks in real-time
7. ✅ Customize theme and add features

## Support

- **Frontend Issues**: Check browser console for errors
- **API Issues**: Check terminal output from `dashboard_api.py`
- **Connection Issues**: Verify both servers are running
- **Data Issues**: Ensure organization is created first

---

**Your AI organization now has a beautiful dashboard!** 🎨✨
