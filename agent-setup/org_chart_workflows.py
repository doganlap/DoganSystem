"""
Module-Specific Workflows for ERPNext Organizational Chart
Defines workflows for each department/module
"""

import logging
from typing import Dict, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModuleWorkflows:
    """Module-specific workflow definitions"""

    @staticmethod
    def get_crm_workflows() -> List[Dict]:
        """CRM module workflows"""
        return [
            {
                "workflow_id": "crm_lead_processing",
                "name": "Daily Lead Processing",
                "department": "CRM",
                "schedule": "daily_9am",
                "assigned_to": "emp_crm_lead_001",
                "subagent_type": "general-purpose",
                "task": """
                Process new leads:
                1. Review all new leads from yesterday
                2. Qualify leads based on criteria
                3. Assign qualified leads to sales team
                4. Send automated follow-up emails
                5. Update lead status
                """
            },
            {
                "workflow_id": "crm_customer_data_cleanup",
                "name": "Weekly Customer Data Cleanup",
                "department": "CRM",
                "schedule": "weekly_friday",
                "assigned_to": "emp_crm_cust_001",
                "subagent_type": "general-purpose",
                "task": """
                Clean up customer data:
                1. Identify duplicate customer records
                2. Merge duplicate customers
                3. Update missing contact information
                4. Verify customer addresses
                5. Generate cleanup report
                """
            },
            {
                "workflow_id": "crm_pipeline_analysis",
                "name": "Weekly Pipeline Analysis",
                "department": "CRM",
                "schedule": "weekly_monday",
                "assigned_to": "emp_crm_analyst_001",
                "subagent_type": "Explore",
                "task": """
                Analyze sales pipeline:
                1. Review all open opportunities
                2. Calculate conversion rates
                3. Identify bottlenecks
                4. Generate pipeline report
                5. Suggest optimization strategies
                """
            }
        ]

    @staticmethod
    def get_sales_workflows() -> List[Dict]:
        """Sales module workflows"""
        return [
            {
                "workflow_id": "sales_quotation_followup",
                "name": "Daily Quotation Follow-up",
                "department": "Sales",
                "schedule": "daily_10am",
                "assigned_to": "emp_sales_quote_001",
                "subagent_type": "general-purpose",
                "task": """
                Follow up on pending quotations:
                1. Find quotations pending for >3 days
                2. Check customer response status
                3. Send follow-up emails
                4. Update quotation status
                5. Create follow-up tasks for sales team
                """
            },
            {
                "workflow_id": "sales_order_processing",
                "name": "Hourly Sales Order Processing",
                "department": "Sales",
                "schedule": "hourly",
                "assigned_to": "emp_sales_order_001",
                "subagent_type": "general-purpose",
                "task": """
                Process new sales orders:
                1. Review newly submitted orders
                2. Verify stock availability
                3. Check credit limits
                4. Create delivery notes for ready orders
                5. Send order confirmation emails
                """
            },
            {
                "workflow_id": "sales_invoice_generation",
                "name": "Daily Invoice Generation",
                "department": "Sales",
                "schedule": "daily_2pm",
                "assigned_to": "emp_sales_inv_001",
                "subagent_type": "general-purpose",
                "task": """
                Generate sales invoices:
                1. Find delivered orders without invoices
                2. Generate invoices for completed deliveries
                3. Apply pricing rules and discounts
                4. Send invoices to customers
                5. Log all invoice emails
                """
            },
            {
                "workflow_id": "sales_performance_analysis",
                "name": "Weekly Sales Analysis",
                "department": "Sales",
                "schedule": "weekly_monday",
                "assigned_to": "emp_sales_analyst_001",
                "subagent_type": "Explore",
                "task": """
                Analyze sales performance:
                1. Calculate weekly sales totals
                2. Analyze by product category
                3. Identify top customers
                4. Compare to targets
                5. Generate executive summary
                """
            },
            {
                "workflow_id": "sales_month_end_closing",
                "name": "Monthly Sales Closing",
                "department": "Sales",
                "schedule": "monthly_last_day",
                "assigned_to": "emp_sales_dir_001",
                "subagent_type": "Plan",
                "task": """
                Month-end sales closing:
                1. Review all pending quotations
                2. Close expired quotations
                3. Generate monthly sales report
                4. Calculate commissions
                5. Prepare executive presentation
                """
            }
        ]

    @staticmethod
    def get_procurement_workflows() -> List[Dict]:
        """Procurement module workflows"""
        return [
            {
                "workflow_id": "buy_reorder_automation",
                "name": "Daily Reorder Processing",
                "department": "Procurement",
                "schedule": "daily_8am",
                "assigned_to": "emp_buy_po_001",
                "subagent_type": "general-purpose",
                "task": """
                Process reorder items:
                1. Check stock levels against reorder points
                2. Generate purchase requests for low stock
                3. Identify preferred suppliers
                4. Create draft purchase orders
                5. Send to procurement for approval
                """
            },
            {
                "workflow_id": "buy_po_followup",
                "name": "PO Delivery Follow-up",
                "department": "Procurement",
                "schedule": "daily_11am",
                "assigned_to": "emp_buy_po_001",
                "subagent_type": "general-purpose",
                "task": """
                Follow up on purchase orders:
                1. Find overdue purchase orders
                2. Send reminders to suppliers
                3. Update expected delivery dates
                4. Escalate delayed orders
                5. Generate delay report
                """
            },
            {
                "workflow_id": "buy_spend_analysis",
                "name": "Monthly Spend Analysis",
                "department": "Procurement",
                "schedule": "monthly_5th",
                "assigned_to": "emp_buy_analyst_001",
                "subagent_type": "Explore",
                "task": """
                Analyze procurement spend:
                1. Calculate total spend by supplier
                2. Analyze by category
                3. Identify cost savings opportunities
                4. Review supplier performance
                5. Generate procurement dashboard
                """
            }
        ]

    @staticmethod
    def get_inventory_workflows() -> List[Dict]:
        """Inventory module workflows"""
        return [
            {
                "workflow_id": "inv_stock_check",
                "name": "Daily Stock Level Check",
                "department": "Inventory",
                "schedule": "daily_7am",
                "assigned_to": "emp_inv_wh_001",
                "subagent_type": "general-purpose",
                "task": """
                Check stock levels:
                1. Review stock levels for all warehouses
                2. Identify items below safety stock
                3. Check for negative stock (errors)
                4. Generate stock alert report
                5. Notify procurement team
                """
            },
            {
                "workflow_id": "inv_reconciliation",
                "name": "Weekly Stock Reconciliation",
                "department": "Inventory",
                "schedule": "weekly_saturday",
                "assigned_to": "emp_inv_stock_001",
                "subagent_type": "general-purpose",
                "task": """
                Perform stock reconciliation:
                1. Compare system stock vs physical count
                2. Identify discrepancies
                3. Create stock reconciliation entries
                4. Update stock balances
                5. Generate reconciliation report
                """
            },
            {
                "workflow_id": "inv_movement_analysis",
                "name": "Monthly Inventory Analysis",
                "department": "Inventory",
                "schedule": "monthly_1st",
                "assigned_to": "emp_inv_analyst_001",
                "subagent_type": "Explore",
                "task": """
                Analyze inventory movements:
                1. Calculate stock turnover ratio
                2. Identify slow-moving items
                3. Identify fast-moving items
                4. Calculate holding costs
                5. Generate optimization recommendations
                """
            }
        ]

    @staticmethod
    def get_accounting_workflows() -> List[Dict]:
        """Accounting module workflows"""
        return [
            {
                "workflow_id": "acc_payment_matching",
                "name": "Daily Payment Matching",
                "department": "Finance",
                "schedule": "daily_3pm",
                "assigned_to": "emp_acc_ar_001",
                "subagent_type": "general-purpose",
                "task": """
                Match payments to invoices:
                1. Review unallocated payments
                2. Match to outstanding invoices
                3. Create payment entries
                4. Update invoice status
                5. Generate matching report
                """
            },
            {
                "workflow_id": "acc_aging_report",
                "name": "Weekly AR Aging",
                "department": "Finance",
                "schedule": "weekly_thursday",
                "assigned_to": "emp_acc_ar_001",
                "subagent_type": "general-purpose",
                "task": """
                Generate accounts receivable aging:
                1. Calculate aging for all customers
                2. Identify overdue amounts
                3. Send payment reminders
                4. Generate collection report
                5. Update credit hold status
                """
            },
            {
                "workflow_id": "acc_month_end",
                "name": "Month-End Close",
                "department": "Finance",
                "schedule": "monthly_last_day",
                "assigned_to": "emp_acc_dir_001",
                "subagent_type": "Plan",
                "task": """
                Month-end closing procedures:
                1. Review all unposted entries
                2. Post month-end journal entries
                3. Run trial balance
                4. Generate financial statements
                5. Close accounting period
                """
            },
            {
                "workflow_id": "acc_financial_analysis",
                "name": "Monthly Financial Analysis",
                "department": "Finance",
                "schedule": "monthly_3rd",
                "assigned_to": "emp_acc_analyst_001",
                "subagent_type": "Explore",
                "task": """
                Analyze financial performance:
                1. Calculate key financial ratios
                2. Compare actual vs budget
                3. Analyze variance
                4. Identify trends
                5. Generate CFO dashboard
                """
            }
        ]

    @staticmethod
    def get_hr_workflows() -> List[Dict]:
        """HR module workflows"""
        return [
            {
                "workflow_id": "hr_attendance_processing",
                "name": "Daily Attendance Processing",
                "department": "HR",
                "schedule": "daily_5pm",
                "assigned_to": "emp_hr_attend_001",
                "subagent_type": "general-purpose",
                "task": """
                Process daily attendance:
                1. Import attendance data
                2. Identify missing check-ins/check-outs
                3. Calculate overtime
                4. Flag attendance issues
                5. Generate attendance report
                """
            },
            {
                "workflow_id": "hr_payroll_processing",
                "name": "Monthly Payroll",
                "department": "HR",
                "schedule": "monthly_25th",
                "assigned_to": "emp_hr_payroll_001",
                "subagent_type": "general-purpose",
                "task": """
                Process monthly payroll:
                1. Calculate salaries for all employees
                2. Apply deductions and benefits
                3. Generate salary slips
                4. Create payment entries
                5. Send salary slips to employees
                """
            },
            {
                "workflow_id": "hr_leave_approval",
                "name": "Daily Leave Processing",
                "department": "HR",
                "schedule": "daily_9am",
                "assigned_to": "emp_hr_attend_001",
                "subagent_type": "general-purpose",
                "task": """
                Process leave applications:
                1. Review pending leave requests
                2. Check leave balances
                3. Auto-approve eligible leaves
                4. Escalate complex cases
                5. Send approval notifications
                """
            }
        ]

    @staticmethod
    def get_projects_workflows() -> List[Dict]:
        """Projects module workflows"""
        return [
            {
                "workflow_id": "pm_task_updates",
                "name": "Daily Task Status Updates",
                "department": "PMO",
                "schedule": "daily_4pm",
                "assigned_to": "emp_pm_001",
                "subagent_type": "general-purpose",
                "task": """
                Update project tasks:
                1. Review task progress
                2. Identify overdue tasks
                3. Send reminders to assignees
                4. Update project status
                5. Generate daily status report
                """
            },
            {
                "workflow_id": "pm_weekly_review",
                "name": "Weekly Project Review",
                "department": "PMO",
                "schedule": "weekly_friday",
                "assigned_to": "emp_pm_dir_001",
                "subagent_type": "Plan",
                "task": """
                Review project portfolio:
                1. Calculate project health metrics
                2. Identify at-risk projects
                3. Review budget vs actual
                4. Update project timelines
                5. Generate executive summary
                """
            }
        ]

    @staticmethod
    def get_manufacturing_workflows() -> List[Dict]:
        """Manufacturing module workflows"""
        return [
            {
                "workflow_id": "mfg_production_planning",
                "name": "Daily Production Planning",
                "department": "Manufacturing",
                "schedule": "daily_6am",
                "assigned_to": "emp_mfg_plan_001",
                "subagent_type": "Plan",
                "task": """
                Plan daily production:
                1. Review sales orders for production
                2. Check raw material availability
                3. Create production plan
                4. Generate work orders
                5. Schedule production
                """
            },
            {
                "workflow_id": "mfg_wo_completion",
                "name": "Work Order Completion",
                "department": "Manufacturing",
                "schedule": "hourly",
                "assigned_to": "emp_mfg_wo_001",
                "subagent_type": "general-purpose",
                "task": """
                Process completed work orders:
                1. Review completed job cards
                2. Update work order progress
                3. Create stock entries for finished goods
                4. Calculate production costs
                5. Close completed work orders
                """
            }
        ]

    @staticmethod
    def get_support_workflows() -> List[Dict]:
        """Support module workflows"""
        return [
            {
                "workflow_id": "sup_ticket_assignment",
                "name": "Hourly Ticket Assignment",
                "department": "Support",
                "schedule": "hourly",
                "assigned_to": "emp_sup_lead_001",
                "subagent_type": "general-purpose",
                "task": """
                Assign support tickets:
                1. Review new unassigned tickets
                2. Categorize by priority and type
                3. Assign to available specialists
                4. Send assignment notifications
                5. Update SLA timers
                """
            },
            {
                "workflow_id": "sup_sla_monitoring",
                "name": "SLA Breach Monitoring",
                "department": "Support",
                "schedule": "every_30min",
                "assigned_to": "emp_sup_lead_001",
                "subagent_type": "general-purpose",
                "task": """
                Monitor SLA compliance:
                1. Check tickets approaching SLA breach
                2. Send escalation alerts
                3. Reassign critical tickets
                4. Update customer on delays
                5. Generate SLA report
                """
            }
        ]

    @staticmethod
    def get_quality_workflows() -> List[Dict]:
        """Quality module workflows"""
        return [
            {
                "workflow_id": "qc_inspection_scheduling",
                "name": "Daily Inspection Scheduling",
                "department": "Quality",
                "schedule": "daily_7am",
                "assigned_to": "emp_qc_insp_001",
                "subagent_type": "general-purpose",
                "task": """
                Schedule quality inspections:
                1. Identify items requiring inspection
                2. Assign inspectors
                3. Create inspection records
                4. Schedule inspection time
                5. Send inspection notifications
                """
            },
            {
                "workflow_id": "qc_defect_analysis",
                "name": "Weekly Defect Analysis",
                "department": "Quality",
                "schedule": "weekly_friday",
                "assigned_to": "emp_qc_dir_001",
                "subagent_type": "Explore",
                "task": """
                Analyze quality defects:
                1. Review all defect reports
                2. Categorize by type and cause
                3. Calculate defect rates
                4. Identify trends
                5. Generate quality improvement plan
                """
            }
        ]

    @staticmethod
    def get_it_workflows() -> List[Dict]:
        """IT module workflows"""
        return [
            {
                "workflow_id": "it_system_health",
                "name": "Daily System Health Check",
                "department": "IT",
                "schedule": "daily_6am",
                "assigned_to": "emp_it_admin_001",
                "subagent_type": "Explore",
                "task": """
                Check ERPNext system health:
                1. Review system error logs
                2. Check database size and performance
                3. Verify scheduled jobs status
                4. Test critical workflows
                5. Generate health report
                """
            },
            {
                "workflow_id": "it_customization_review",
                "name": "Weekly Customization Review",
                "department": "IT",
                "schedule": "weekly_monday",
                "assigned_to": "emp_it_dev_001",
                "subagent_type": "Plan",
                "task": """
                Review system customizations:
                1. Audit custom fields added
                2. Review custom scripts
                3. Check for deprecated code
                4. Test custom workflows
                5. Generate customization report
                """
            },
            {
                "workflow_id": "it_data_analysis",
                "name": "Monthly Data Analysis",
                "department": "IT",
                "schedule": "monthly_1st",
                "assigned_to": "emp_it_analyst_001",
                "subagent_type": "Explore",
                "task": """
                Analyze system data:
                1. Review data growth trends
                2. Identify data quality issues
                3. Analyze usage patterns
                4. Optimize database performance
                5. Generate insights report
                """
            }
        ]

    @staticmethod
    def get_all_workflows() -> Dict[str, List[Dict]]:
        """Get all module workflows"""
        return {
            "CRM": ModuleWorkflows.get_crm_workflows(),
            "Sales": ModuleWorkflows.get_sales_workflows(),
            "Procurement": ModuleWorkflows.get_procurement_workflows(),
            "Inventory": ModuleWorkflows.get_inventory_workflows(),
            "Accounting": ModuleWorkflows.get_accounting_workflows(),
            "HR": ModuleWorkflows.get_hr_workflows(),
            "Projects": ModuleWorkflows.get_projects_workflows(),
            "Manufacturing": ModuleWorkflows.get_manufacturing_workflows(),
            "Support": ModuleWorkflows.get_support_workflows(),
            "Quality": ModuleWorkflows.get_quality_workflows(),
            "IT": ModuleWorkflows.get_it_workflows()
        }

    @staticmethod
    def get_workflow_summary() -> Dict:
        """Get summary of all workflows"""
        all_workflows = ModuleWorkflows.get_all_workflows()

        total = sum(len(workflows) for workflows in all_workflows.values())

        by_schedule = {}
        by_subagent = {}

        for module, workflows in all_workflows.items():
            for wf in workflows:
                schedule = wf["schedule"]
                if schedule not in by_schedule:
                    by_schedule[schedule] = 0
                by_schedule[schedule] += 1

                subagent = wf["subagent_type"]
                if subagent not in by_subagent:
                    by_subagent[subagent] = 0
                by_subagent[subagent] += 1

        return {
            "total_workflows": total,
            "by_module": {module: len(workflows) for module, workflows in all_workflows.items()},
            "by_schedule": by_schedule,
            "by_subagent": by_subagent
        }


# Example usage
if __name__ == "__main__":
    import json

    print("\n" + "="*80)
    print("ERPNEXT MODULE WORKFLOWS")
    print("="*80 + "\n")

    summary = ModuleWorkflows.get_workflow_summary()

    print("WORKFLOW SUMMARY:")
    print("-" * 80)
    print(json.dumps(summary, indent=2))

    print("\n\nSAMPLE WORKFLOWS BY MODULE:")
    print("-" * 80)

    all_workflows = ModuleWorkflows.get_all_workflows()
    for module, workflows in all_workflows.items():
        print(f"\n{module} ({len(workflows)} workflows):")
        for wf in workflows[:2]:  # Show first 2 workflows
            print(f"  - {wf['name']}")
            print(f"    Schedule: {wf['schedule']}")
            print(f"    Assigned to: {wf['assigned_to']}")
