"""
Database Models and ORM Layer
SQLAlchemy models for the complete system
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from decimal import Decimal as PyDecimal
from sqlalchemy import (
    create_engine, Column, String, Integer, DateTime, Boolean,
    Text, Date, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.types import DECIMAL as Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()


# ===== EMPLOYEES & ORGANIZATION =====

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(String(50), primary_key=True)
    employee_name = Column(String(200), nullable=False)
    employee_name_en = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))

    # Role & Position
    title = Column(String(200), nullable=False)
    role = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    level = Column(String(50))

    # Subagent Configuration
    subagent_type = Column(String(50), nullable=False)
    status = Column(String(50), default='available')

    # Organization Hierarchy
    manager_id = Column(String(50), ForeignKey('employees.employee_id'))
    team_id = Column(String(50), ForeignKey('teams.team_id'))

    # Metadata
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_active = Column(DateTime)

    # Relationships
    manager = relationship('Employee', remote_side=[employee_id], backref='direct_reports', foreign_keys=[manager_id])
    team = relationship('Team', back_populates='members', foreign_keys=[team_id])
    capabilities = relationship('EmployeeCapability', back_populates='employee')
    roles = relationship('EmployeeRole', back_populates='employee')
    tasks = relationship('Task', back_populates='employee')

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'employee_name_en': self.employee_name_en,
            'email': self.email,
            'title': self.title,
            'role': self.role,
            'department': self.department,
            'level': self.level,
            'subagent_type': self.subagent_type,
            'status': self.status,
            'manager_id': self.manager_id,
            'team_id': self.team_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(String(50), primary_key=True)
    department_name = Column(String(100), nullable=False, unique=True)
    department_name_ar = Column(String(100))
    description = Column(Text)
    erpnext_module = Column(String(100))

    parent_department_id = Column(String(50), ForeignKey('departments.department_id'))
    head_employee_id = Column(String(50), ForeignKey('employees.employee_id'))

    email = Column(String(200))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    parent = relationship('Department', remote_side=[department_id], backref='sub_departments')
    teams = relationship('Team', back_populates='department')


class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(String(50), primary_key=True)
    team_name = Column(String(100), nullable=False)
    department_id = Column(String(50), ForeignKey('departments.department_id'), nullable=False)
    description = Column(Text)
    team_lead_id = Column(String(50), ForeignKey('employees.employee_id'))
    primary_function = Column(String(200))
    objectives = Column(Text)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    department = relationship('Department', back_populates='teams')
    members = relationship('Employee', back_populates='team', foreign_keys='Employee.team_id')
    team_lead = relationship('Employee', foreign_keys=[team_lead_id])


# ===== ROLES & RESPONSIBILITIES =====

class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(String(50), primary_key=True)
    role_name = Column(String(100), nullable=False, unique=True)
    role_description = Column(Text)
    level = Column(String(50))
    department = Column(String(100))

    # Permissions
    can_approve_workflows = Column(Boolean, default=False)
    can_manage_employees = Column(Boolean, default=False)
    can_execute_tasks = Column(Boolean, default=False)
    can_view_analytics = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    responsibilities = relationship('Responsibility', back_populates='role')
    employee_roles = relationship('EmployeeRole', back_populates='role')


class Responsibility(Base):
    __tablename__ = 'responsibilities'

    responsibility_id = Column(String(50), primary_key=True)
    role_id = Column(String(50), ForeignKey('roles.role_id'), nullable=False)

    responsibility_name = Column(String(200), nullable=False)
    responsibility_description = Column(Text)
    scope = Column(Text)
    priority = Column(Integer, default=0)

    category = Column(String(100))
    frequency = Column(String(50))

    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    role = relationship('Role', back_populates='responsibilities')


class EmployeeRole(Base):
    __tablename__ = 'employee_roles'

    employee_id = Column(String(50), ForeignKey('employees.employee_id'), primary_key=True)
    role_id = Column(String(50), ForeignKey('roles.role_id'), primary_key=True)
    assigned_at = Column(DateTime, default=datetime.now)
    is_primary = Column(Boolean, default=False)

    # Relationships
    employee = relationship('Employee', back_populates='roles')
    role = relationship('Role', back_populates='employee_roles')


# ===== CAPABILITIES & SCOPE =====

class Capability(Base):
    __tablename__ = 'capabilities'

    capability_id = Column(String(50), primary_key=True)
    capability_name = Column(String(200), nullable=False, unique=True)
    capability_description = Column(Text)
    category = Column(String(100))
    skill_level = Column(String(50))
    erpnext_module = Column(String(100))
    erpnext_doctype = Column(String(100))

    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    employee_capabilities = relationship('EmployeeCapability', back_populates='capability')


class EmployeeCapability(Base):
    __tablename__ = 'employee_capabilities'

    employee_id = Column(String(50), ForeignKey('employees.employee_id'), primary_key=True)
    capability_id = Column(String(50), ForeignKey('capabilities.capability_id'), primary_key=True)
    proficiency_level = Column(String(50), default='intermediate')
    acquired_at = Column(DateTime, default=datetime.now)
    last_used = Column(DateTime)

    # Relationships
    employee = relationship('Employee', back_populates='capabilities')
    capability = relationship('Capability', back_populates='employee_capabilities')


class Scope(Base):
    __tablename__ = 'scopes'

    scope_id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id'), nullable=False)

    scope_name = Column(String(200), nullable=False)
    scope_description = Column(Text)
    scope_type = Column(String(50))

    erpnext_modules = Column(Text)  # JSON
    customer_segments = Column(Text)  # JSON
    geographical_areas = Column(Text)  # JSON

    budget_limit = Column(Decimal(15, 2))
    approval_required = Column(Boolean, default=False)

    effective_from = Column(Date)
    effective_to = Column(Date)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# ===== WORKFLOWS & TASKS =====

class Workflow(Base):
    __tablename__ = 'workflows'

    workflow_id = Column(String(50), primary_key=True)
    workflow_name = Column(String(200), nullable=False)
    description = Column(Text)
    department = Column(String(100))
    assigned_employee_id = Column(String(50), ForeignKey('employees.employee_id'))

    schedule_type = Column(String(50))
    schedule_config = Column(Text)  # JSON

    subagent_type = Column(String(50), nullable=False)
    task_template = Column(Text, nullable=False)

    is_enabled = Column(Boolean, default=True)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    execution_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    tasks = relationship('Task', back_populates='workflow')


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String(50), primary_key=True)
    workflow_id = Column(String(50), ForeignKey('workflows.workflow_id'))
    employee_id = Column(String(50), ForeignKey('employees.employee_id'), nullable=False)
    employee_name = Column(String(200))

    task_description = Column(Text, nullable=False)
    subagent_type = Column(String(50), nullable=False)

    status = Column(String(50), default='pending')
    progress = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.now)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)

    result = Column(Text)  # JSON
    error_message = Column(Text)

    priority = Column(Integer, default=0)
    tags = Column(Text)  # JSON

    # Relationships
    workflow = relationship('Workflow', back_populates='tasks')
    employee = relationship('Employee', back_populates='tasks')

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'workflow_id': self.workflow_id,
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'task_description': self.task_description[:200],
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


# ===== PERFORMANCE & ANALYTICS =====

class EmployeeMetrics(Base):
    __tablename__ = 'employee_metrics'

    metric_id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id'), nullable=False)

    metric_date = Column(Date, nullable=False)
    period_type = Column(String(50))

    tasks_completed = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)
    tasks_pending = Column(Integer, default=0)
    avg_task_duration_seconds = Column(Integer)
    success_rate = Column(Decimal(5, 2))

    total_work_hours = Column(Decimal(10, 2))
    utilization_rate = Column(Decimal(5, 2))

    quality_score = Column(Decimal(5, 2))
    error_rate = Column(Decimal(5, 2))

    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint('employee_id', 'metric_date', 'period_type'),
    )


# ===== NOTIFICATIONS =====

class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.employee_id'))
    department_id = Column(String(50), ForeignKey('departments.department_id'))

    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))
    category = Column(String(50))

    related_task_id = Column(String(50), ForeignKey('tasks.task_id'))
    related_workflow_id = Column(String(50), ForeignKey('workflows.workflow_id'))

    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)

    action_url = Column(String(500))
    action_label = Column(String(100))

    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime)


# ===== AUDIT & LOGGING =====

class AuditLog(Base):
    __tablename__ = 'audit_log'

    audit_id = Column(String(50), primary_key=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)

    old_values = Column(Text)  # JSON
    new_values = Column(Text)  # JSON
    changed_fields = Column(Text)  # JSON

    changed_by = Column(String(50))
    changed_at = Column(DateTime, default=datetime.now)

    reason = Column(Text)
    ip_address = Column(String(50))
    user_agent = Column(Text)


class SystemEvent(Base):
    __tablename__ = 'system_events'

    event_id = Column(String(50), primary_key=True)
    event_type = Column(String(100), nullable=False)
    event_category = Column(String(50))
    event_severity = Column(String(50), default='info')

    event_message = Column(Text, nullable=False)
    event_data = Column(Text)  # JSON

    source_component = Column(String(100))
    source_id = Column(String(50))

    created_at = Column(DateTime, default=datetime.now)


# ===== DATABASE CLASS =====

class Database:
    """Database management class"""

    def __init__(self, db_url: str = None):
        if db_url is None:
            db_url = os.getenv('DATABASE_URL', 'sqlite:///dogansystem.db')

        self.engine = create_engine(
            db_url,
            echo=False,
            connect_args={'check_same_thread': False} if 'sqlite' in db_url else {},
            poolclass=StaticPool if 'sqlite' in db_url else None
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Drop all tables"""
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()


# Initialize database
db = Database()


if __name__ == "__main__":
    print("Creating database tables...")
    db.create_tables()
    print("✓ Tables created successfully")
