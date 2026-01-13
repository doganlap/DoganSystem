-- =====================================================
-- DoganSystem Complete Database Schema
-- AI Employee Organization Management System
-- =====================================================

-- =====================================================
-- 1. EMPLOYEES & ORGANIZATION
-- =====================================================

-- Main employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    employee_name VARCHAR(200) NOT NULL,
    employee_name_en VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),

    -- Role & Position
    title VARCHAR(200) NOT NULL,
    role VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    level VARCHAR(50), -- C-Level, Director, Manager, Specialist, Analyst

    -- Subagent Configuration
    subagent_type VARCHAR(50) NOT NULL, -- Explore, Plan, general-purpose
    status VARCHAR(50) DEFAULT 'available', -- available, busy, away, offline

    -- Organization Hierarchy
    manager_id VARCHAR(50),
    team_id VARCHAR(50),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP,

    FOREIGN KEY (manager_id) REFERENCES employees(employee_id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
);

-- Index for common queries
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department);
CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status);
CREATE INDEX IF NOT EXISTS idx_employees_type ON employees(subagent_type);
CREATE INDEX IF NOT EXISTS idx_employees_manager ON employees(manager_id);

-- =====================================================
-- 2. ROLES & RESPONSIBILITIES
-- =====================================================

-- Roles definition table
CREATE TABLE IF NOT EXISTS roles (
    role_id VARCHAR(50) PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    role_description TEXT,
    level VARCHAR(50), -- Executive, Director, Manager, Specialist
    department VARCHAR(100),

    -- Permissions
    can_approve_workflows BOOLEAN DEFAULT FALSE,
    can_manage_employees BOOLEAN DEFAULT FALSE,
    can_execute_tasks BOOLEAN DEFAULT FALSE,
    can_view_analytics BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Responsibilities table
CREATE TABLE IF NOT EXISTS responsibilities (
    responsibility_id VARCHAR(50) PRIMARY KEY,
    role_id VARCHAR(50) NOT NULL,

    -- Responsibility Details
    responsibility_name VARCHAR(200) NOT NULL,
    responsibility_description TEXT,
    scope TEXT, -- What this responsibility covers
    priority INTEGER DEFAULT 0, -- Higher = more important

    -- Classification
    category VARCHAR(100), -- Strategic, Operational, Administrative
    frequency VARCHAR(50), -- Daily, Weekly, Monthly, As-needed

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_responsibilities_role ON responsibilities(role_id);

-- Employee-Role mapping (employees can have multiple roles)
CREATE TABLE IF NOT EXISTS employee_roles (
    employee_id VARCHAR(50) NOT NULL,
    role_id VARCHAR(50) NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_primary BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (employee_id, role_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
);

-- =====================================================
-- 3. CAPABILITIES & SCOPE
-- =====================================================

-- Capabilities definition
CREATE TABLE IF NOT EXISTS capabilities (
    capability_id VARCHAR(50) PRIMARY KEY,
    capability_name VARCHAR(200) NOT NULL UNIQUE,
    capability_description TEXT,

    -- Classification
    category VARCHAR(100), -- Technical, Business, Analytical, Communication
    skill_level VARCHAR(50), -- Basic, Intermediate, Advanced, Expert

    -- ERPNext Module relationship
    erpnext_module VARCHAR(100), -- Sales, CRM, Inventory, etc.
    erpnext_doctype VARCHAR(100), -- Customer, Sales Order, etc.

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employee capabilities (what each employee can do)
CREATE TABLE IF NOT EXISTS employee_capabilities (
    employee_id VARCHAR(50) NOT NULL,
    capability_id VARCHAR(50) NOT NULL,
    proficiency_level VARCHAR(50) DEFAULT 'intermediate', -- basic, intermediate, advanced, expert
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP,

    PRIMARY KEY (employee_id, capability_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (capability_id) REFERENCES capabilities(capability_id) ON DELETE CASCADE
);

-- Scope definitions (what areas each employee covers)
CREATE TABLE IF NOT EXISTS scopes (
    scope_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,

    -- Scope Details
    scope_name VARCHAR(200) NOT NULL,
    scope_description TEXT,
    scope_type VARCHAR(50), -- Geographic, Functional, Product, Customer

    -- Coverage
    erpnext_modules TEXT, -- JSON array of modules
    customer_segments TEXT, -- JSON array
    geographical_areas TEXT, -- JSON array

    -- Constraints
    budget_limit DECIMAL(15,2),
    approval_required BOOLEAN DEFAULT FALSE,

    effective_from DATE,
    effective_to DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scopes_employee ON scopes(employee_id);

-- =====================================================
-- 4. ORGANIZATIONAL STRUCTURE
-- =====================================================

-- Departments
CREATE TABLE IF NOT EXISTS departments (
    department_id VARCHAR(50) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    department_name_ar VARCHAR(100),
    description TEXT,

    -- ERPNext Module mapping
    erpnext_module VARCHAR(100),

    -- Hierarchy
    parent_department_id VARCHAR(50),
    head_employee_id VARCHAR(50), -- Department head

    -- Contact
    email VARCHAR(200),
    phone VARCHAR(50),

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (parent_department_id) REFERENCES departments(department_id) ON DELETE SET NULL,
    FOREIGN KEY (head_employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

-- Teams within departments
CREATE TABLE IF NOT EXISTS teams (
    team_id VARCHAR(50) PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    department_id VARCHAR(50) NOT NULL,

    -- Team Details
    description TEXT,
    team_lead_id VARCHAR(50),

    -- Purpose
    primary_function VARCHAR(200),
    objectives TEXT,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE,
    FOREIGN KEY (team_lead_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_teams_department ON teams(department_id);

-- Team members
CREATE TABLE IF NOT EXISTS team_members (
    team_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(50) NOT NULL,
    role_in_team VARCHAR(100), -- Lead, Member, Specialist
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (team_id, employee_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

-- =====================================================
-- 5. WORKFLOWS & TASKS
-- =====================================================

-- Workflow definitions
CREATE TABLE IF NOT EXISTS workflows (
    workflow_id VARCHAR(50) PRIMARY KEY,
    workflow_name VARCHAR(200) NOT NULL,
    description TEXT,

    -- Assignment
    department VARCHAR(100),
    assigned_employee_id VARCHAR(50),

    -- Scheduling
    schedule_type VARCHAR(50), -- hourly, daily, weekly, monthly, manual
    schedule_config TEXT, -- JSON configuration

    -- Execution
    subagent_type VARCHAR(50) NOT NULL, -- Explore, Plan, general-purpose
    task_template TEXT NOT NULL, -- Task description template

    -- Status
    is_enabled BOOLEAN DEFAULT TRUE,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    execution_count INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (assigned_employee_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_workflows_department ON workflows(department);
CREATE INDEX IF NOT EXISTS idx_workflows_enabled ON workflows(is_enabled);

-- Task execution history
CREATE TABLE IF NOT EXISTS tasks (
    task_id VARCHAR(50) PRIMARY KEY,
    workflow_id VARCHAR(50),

    -- Assignment
    employee_id VARCHAR(50) NOT NULL,
    employee_name VARCHAR(200),

    -- Task Details
    task_description TEXT NOT NULL,
    subagent_type VARCHAR(50) NOT NULL,

    -- Execution
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, failed
    progress INTEGER DEFAULT 0, -- 0-100

    -- Timing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    -- Results
    result TEXT, -- JSON result data
    error_message TEXT,

    -- Metadata
    priority INTEGER DEFAULT 0,
    tags TEXT, -- JSON array

    FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id) ON DELETE SET NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tasks_employee ON tasks(employee_id);
CREATE INDEX IF NOT EXISTS idx_tasks_workflow ON tasks(workflow_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at);

-- Task dependencies
CREATE TABLE IF NOT EXISTS task_dependencies (
    task_id VARCHAR(50) NOT NULL,
    depends_on_task_id VARCHAR(50) NOT NULL,
    dependency_type VARCHAR(50) DEFAULT 'finish_to_start', -- finish_to_start, start_to_start

    PRIMARY KEY (task_id, depends_on_task_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(task_id) ON DELETE CASCADE
);

-- =====================================================
-- 6. PERFORMANCE & ANALYTICS
-- =====================================================

-- Employee performance metrics
CREATE TABLE IF NOT EXISTS employee_metrics (
    metric_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,

    -- Period
    metric_date DATE NOT NULL,
    period_type VARCHAR(50), -- daily, weekly, monthly

    -- Task Metrics
    tasks_completed INTEGER DEFAULT 0,
    tasks_failed INTEGER DEFAULT 0,
    tasks_pending INTEGER DEFAULT 0,
    avg_task_duration_seconds INTEGER,
    success_rate DECIMAL(5,2),

    -- Workload
    total_work_hours DECIMAL(10,2),
    utilization_rate DECIMAL(5,2),

    -- Quality
    quality_score DECIMAL(5,2),
    error_rate DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    UNIQUE (employee_id, metric_date, period_type)
);

CREATE INDEX IF NOT EXISTS idx_metrics_employee ON employee_metrics(employee_id);
CREATE INDEX IF NOT EXISTS idx_metrics_date ON employee_metrics(metric_date);

-- Department performance
CREATE TABLE IF NOT EXISTS department_metrics (
    metric_id VARCHAR(50) PRIMARY KEY,
    department_id VARCHAR(50) NOT NULL,

    -- Period
    metric_date DATE NOT NULL,
    period_type VARCHAR(50),

    -- Team Metrics
    total_employees INTEGER,
    active_employees INTEGER,
    total_tasks INTEGER,
    completed_tasks INTEGER,
    avg_completion_time_seconds INTEGER,

    -- Performance
    department_efficiency DECIMAL(5,2),
    overall_quality DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE,
    UNIQUE (department_id, metric_date, period_type)
);

-- =====================================================
-- 7. ERPNEXT INTEGRATION
-- =====================================================

-- ERPNext module access
CREATE TABLE IF NOT EXISTS erpnext_access (
    access_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,

    -- ERPNext Details
    erpnext_module VARCHAR(100) NOT NULL,
    erpnext_doctype VARCHAR(100),

    -- Permissions
    can_read BOOLEAN DEFAULT TRUE,
    can_create BOOLEAN DEFAULT FALSE,
    can_update BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE,
    can_submit BOOLEAN DEFAULT FALSE,
    can_cancel BOOLEAN DEFAULT FALSE,

    -- Scope
    access_level VARCHAR(50) DEFAULT 'all', -- all, own, department, team

    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by VARCHAR(50),

    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    UNIQUE (employee_id, erpnext_module, erpnext_doctype)
);

CREATE INDEX IF NOT EXISTS idx_erpnext_access_employee ON erpnext_access(employee_id);

-- ERPNext actions log
CREATE TABLE IF NOT EXISTS erpnext_actions (
    action_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(50) NOT NULL,
    task_id VARCHAR(50),

    -- Action Details
    action_type VARCHAR(50) NOT NULL, -- create, read, update, delete, submit
    erpnext_module VARCHAR(100) NOT NULL,
    erpnext_doctype VARCHAR(100) NOT NULL,
    document_name VARCHAR(200),

    -- Execution
    status VARCHAR(50) DEFAULT 'pending', -- pending, success, failed
    request_data TEXT, -- JSON
    response_data TEXT, -- JSON
    error_message TEXT,

    execution_time_ms INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_erpnext_actions_employee ON erpnext_actions(employee_id);
CREATE INDEX IF NOT EXISTS idx_erpnext_actions_task ON erpnext_actions(task_id);
CREATE INDEX IF NOT EXISTS idx_erpnext_actions_created ON erpnext_actions(created_at);

-- =====================================================
-- 8. AUDIT & LOGGING
-- =====================================================

-- Audit trail for all changes
CREATE TABLE IF NOT EXISTS audit_log (
    audit_id VARCHAR(50) PRIMARY KEY,

    -- What changed
    table_name VARCHAR(100) NOT NULL,
    record_id VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE

    -- Changes
    old_values TEXT, -- JSON
    new_values TEXT, -- JSON
    changed_fields TEXT, -- JSON array

    -- Who & When
    changed_by VARCHAR(50), -- employee_id or system
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Context
    reason TEXT,
    ip_address VARCHAR(50),
    user_agent TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_table ON audit_log(table_name);
CREATE INDEX IF NOT EXISTS idx_audit_record ON audit_log(record_id);
CREATE INDEX IF NOT EXISTS idx_audit_date ON audit_log(changed_at);

-- System events log
CREATE TABLE IF NOT EXISTS system_events (
    event_id VARCHAR(50) PRIMARY KEY,

    -- Event Details
    event_type VARCHAR(100) NOT NULL,
    event_category VARCHAR(50), -- system, security, workflow, employee
    event_severity VARCHAR(50) DEFAULT 'info', -- info, warning, error, critical

    -- Description
    event_message TEXT NOT NULL,
    event_data TEXT, -- JSON

    -- Source
    source_component VARCHAR(100), -- api, workflow, employee, system
    source_id VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_type ON system_events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_severity ON system_events(event_severity);
CREATE INDEX IF NOT EXISTS idx_events_date ON system_events(created_at);

-- =====================================================
-- 9. CONFIGURATION & SETTINGS
-- =====================================================

-- System configuration
CREATE TABLE IF NOT EXISTS system_config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value TEXT,
    config_type VARCHAR(50) DEFAULT 'string', -- string, number, boolean, json
    description TEXT,
    category VARCHAR(50), -- system, erpnext, dashboard, workflow

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(50)
);

-- Insert default configurations
INSERT OR IGNORE INTO system_config (config_key, config_value, config_type, description, category) VALUES
('system.name', 'DoganSystem', 'string', 'System name', 'system'),
('system.version', '1.0.0', 'string', 'System version', 'system'),
('erpnext.base_url', 'http://localhost:8000', 'string', 'ERPNext base URL', 'erpnext'),
('dashboard.api_port', '8007', 'number', 'Dashboard API port', 'dashboard'),
('workflow.max_concurrent', '10', 'number', 'Max concurrent workflows', 'workflow'),
('task.default_timeout', '3600', 'number', 'Default task timeout (seconds)', 'workflow');

-- =====================================================
-- 10. NOTIFICATIONS & ALERTS
-- =====================================================

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    notification_id VARCHAR(50) PRIMARY KEY,

    -- Recipient
    employee_id VARCHAR(50),
    department_id VARCHAR(50),

    -- Notification Details
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50), -- info, success, warning, error
    category VARCHAR(50), -- task, workflow, system, alert

    -- Related entities
    related_task_id VARCHAR(50),
    related_workflow_id VARCHAR(50),

    -- Status
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,

    -- Actions
    action_url VARCHAR(500),
    action_label VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE,
    FOREIGN KEY (related_task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (related_workflow_id) REFERENCES workflows(workflow_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_notifications_employee ON notifications(employee_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View: Employee with full details
CREATE VIEW IF NOT EXISTS v_employee_details AS
SELECT
    e.employee_id,
    e.employee_name,
    e.employee_name_en,
    e.email,
    e.title,
    e.role,
    e.department,
    e.level,
    e.subagent_type,
    e.status,
    m.employee_name as manager_name,
    t.team_name,
    d.department_name,
    COUNT(DISTINCT ec.capability_id) as total_capabilities,
    COUNT(DISTINCT er.role_id) as total_roles
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
LEFT JOIN teams t ON e.team_id = t.team_id
LEFT JOIN departments d ON e.department = d.department_id
LEFT JOIN employee_capabilities ec ON e.employee_id = ec.employee_id
LEFT JOIN employee_roles er ON e.employee_id = er.employee_id
GROUP BY e.employee_id;

-- View: Task statistics per employee
CREATE VIEW IF NOT EXISTS v_employee_task_stats AS
SELECT
    e.employee_id,
    e.employee_name,
    COUNT(t.task_id) as total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN t.status = 'failed' THEN 1 ELSE 0 END) as failed_tasks,
    SUM(CASE WHEN t.status = 'in_progress' THEN 1 ELSE 0 END) as active_tasks,
    AVG(CASE WHEN t.status = 'completed' THEN t.duration_seconds END) as avg_duration_seconds
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
GROUP BY e.employee_id;

-- View: Department summary
CREATE VIEW IF NOT EXISTS v_department_summary AS
SELECT
    d.department_id,
    d.department_name,
    COUNT(DISTINCT e.employee_id) as total_employees,
    COUNT(DISTINCT t.team_id) as total_teams,
    COUNT(DISTINCT w.workflow_id) as total_workflows,
    COUNT(DISTINCT tk.task_id) as total_tasks
FROM departments d
LEFT JOIN employees e ON d.department_id = e.department
LEFT JOIN teams t ON d.department_id = t.department_id
LEFT JOIN workflows w ON d.department_id = w.department
LEFT JOIN tasks tk ON e.employee_id = tk.employee_id
GROUP BY d.department_id;

-- =====================================================
-- END OF SCHEMA
-- =====================================================
