"""
ERPNext Complete Organizational Chart
AI Employees for every module in ERPNext
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from claude_code_bridge import SubagentERPNextBridge, SubagentEmployee

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class OrganizationalUnit:
    """Represents a department/module organizational unit"""
    unit_id: str
    name: str
    module: str  # ERPNext module
    description: str
    manager_id: Optional[str] = None
    team_leads: List[str] = None
    specialists: List[str] = None

    def __post_init__(self):
        if self.team_leads is None:
            self.team_leads = []
        if self.specialists is None:
            self.specialists = []


class ERPNextOrgChart:
    """
    Complete organizational chart for ERPNext
    Creates AI employees for all modules with proper hierarchy
    """

    def __init__(self, bridge: SubagentERPNextBridge):
        self.bridge = bridge
        self.org_units: Dict[str, OrganizationalUnit] = {}
        self.employee_registry: Dict[str, Dict] = {}

        # Module definitions
        self.modules = {
            "CRM": {
                "name": "Customer Relationship Management",
                "doctypes": ["Lead", "Opportunity", "Customer", "Contact", "Address"]
            },
            "Sales": {
                "name": "Sales Management",
                "doctypes": ["Quotation", "Sales Order", "Sales Invoice", "Delivery Note"]
            },
            "Buying": {
                "name": "Procurement Management",
                "doctypes": ["Supplier", "Purchase Order", "Purchase Receipt", "Purchase Invoice"]
            },
            "Stock": {
                "name": "Inventory Management",
                "doctypes": ["Item", "Warehouse", "Stock Entry", "Stock Reconciliation"]
            },
            "Accounts": {
                "name": "Financial Accounting",
                "doctypes": ["Account", "Journal Entry", "Payment Entry", "GL Entry"]
            },
            "HR": {
                "name": "Human Resources",
                "doctypes": ["Employee", "Attendance", "Leave Application", "Salary Structure"]
            },
            "Projects": {
                "name": "Project Management",
                "doctypes": ["Project", "Task", "Timesheet", "Project Update"]
            },
            "Manufacturing": {
                "name": "Production Management",
                "doctypes": ["BOM", "Work Order", "Job Card", "Production Plan"]
            },
            "Support": {
                "name": "Customer Support",
                "doctypes": ["Issue", "Service Level Agreement", "Warranty Claim"]
            },
            "Quality": {
                "name": "Quality Management",
                "doctypes": ["Quality Inspection", "Quality Goal", "Quality Procedure"]
            },
            "Assets": {
                "name": "Asset Management",
                "doctypes": ["Asset", "Asset Maintenance", "Asset Repair"]
            },
            "IT": {
                "name": "IT Operations",
                "doctypes": ["System Settings", "Custom Field", "Workflow", "Custom Script"]
            }
        }

    def create_complete_org_chart(self):
        """Create complete organizational chart for all modules"""
        logger.info("Creating complete ERPNext organizational chart...")

        # Create C-level executives
        self._create_executives()

        # Create module departments
        self._create_crm_department()
        self._create_sales_department()
        self._create_buying_department()
        self._create_inventory_department()
        self._create_accounting_department()
        self._create_hr_department()
        self._create_projects_department()
        self._create_manufacturing_department()
        self._create_support_department()
        self._create_quality_department()
        self._create_assets_department()
        self._create_it_department()

        logger.info(f"Organizational chart created with {len(self.employee_registry)} employees")

        return self.get_org_chart_summary()

    def _create_executives(self):
        """Create C-level executives"""
        logger.info("Creating executive team...")

        # CEO - Overall system oversight
        ceo = self.bridge.create_planner_employee(
            employee_name="عبدالله المهندس",  # Abdullah Al-Muhandis
            department="Executive",
            employee_id="emp_ceo_001"
        )
        self._register_employee(ceo, "CEO", None, "Executive leadership and strategic planning")

        # CTO - IT and system architecture
        cto = self.bridge.create_explorer_employee(
            employee_name="نورة التقنية",  # Noura Al-Tiqniya
            department="Executive",
            employee_id="emp_cto_001"
        )
        self._register_employee(cto, "CTO", "emp_ceo_001", "Technology strategy and system architecture")

        # CFO - Financial oversight
        cfo = self.bridge.create_planner_employee(
            employee_name="خالد المالي",  # Khaled Al-Mali
            department="Executive",
            employee_id="emp_cfo_001"
        )
        self._register_employee(cfo, "CFO", "emp_ceo_001", "Financial planning and accounting oversight")

        # COO - Operations management
        coo = self.bridge.create_operations_employee(
            employee_name="ريم العمليات",  # Reem Al-Amaliyat
            department="Executive",
            employee_id="emp_coo_001"
        )
        self._register_employee(coo, "COO", "emp_ceo_001", "Operational excellence and process optimization")

    def _create_crm_department(self):
        """Create CRM department organization"""
        logger.info("Creating CRM department...")

        # CRM Director
        director = self.bridge.create_planner_employee(
            employee_name="سارة العملاء",  # Sarah Al-Omala
            department="CRM",
            employee_id="emp_crm_dir_001"
        )
        self._register_employee(director, "CRM Director", "emp_ceo_001", "Customer relationship strategy")

        # Lead Management Team Lead
        lead_manager = self.bridge.create_operations_employee(
            employee_name="أحمد الفرص",  # Ahmed Al-Furas
            department="CRM",
            employee_id="emp_crm_lead_001"
        )
        self._register_employee(lead_manager, "Lead Management Team Lead", "emp_crm_dir_001", "Lead generation and qualification")

        # Lead Specialists
        for i in range(3):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص الفرص {i+1}",  # Lead Specialist {i+1}
                department="CRM",
                employee_id=f"emp_crm_lead_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Lead Specialist", "emp_crm_lead_001", "Lead processing and follow-up")

        # Customer Management Team Lead
        customer_manager = self.bridge.create_operations_employee(
            employee_name="فاطمة العملاء",  # Fatima Al-Omala
            department="CRM",
            employee_id="emp_crm_cust_001"
        )
        self._register_employee(customer_manager, "Customer Management Team Lead", "emp_crm_dir_001", "Customer data management")

        # Customer Specialists
        for i in range(3):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص العملاء {i+1}",
                department="CRM",
                employee_id=f"emp_crm_cust_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Customer Specialist", "emp_crm_cust_001", "Customer records management")

        # CRM Analyst
        analyst = self.bridge.create_explorer_employee(
            employee_name="ياسر التحليل",  # Yasser Al-Tahlil
            department="CRM",
            employee_id="emp_crm_analyst_001"
        )
        self._register_employee(analyst, "CRM Analyst", "emp_crm_dir_001", "Customer data analysis and insights")

        self._create_org_unit("CRM", "Customer Relationship Management", "CRM",
                             "emp_crm_dir_001",
                             ["emp_crm_lead_001", "emp_crm_cust_001"],
                             ["emp_crm_analyst_001"])

    def _create_sales_department(self):
        """Create Sales department organization"""
        logger.info("Creating Sales department...")

        # Sales Director
        director = self.bridge.create_planner_employee(
            employee_name="محمد المبيعات",  # Mohammed Al-Mabiyat
            department="Sales",
            employee_id="emp_sales_dir_001"
        )
        self._register_employee(director, "Sales Director", "emp_coo_001", "Sales strategy and revenue growth")

        # Quotation Team Lead
        quote_lead = self.bridge.create_operations_employee(
            employee_name="نوف العروض",  # Nouf Al-Orood
            department="Sales",
            employee_id="emp_sales_quote_001"
        )
        self._register_employee(quote_lead, "Quotation Team Lead", "emp_sales_dir_001", "Quotation management")

        # Quotation Specialists
        for i in range(4):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص العروض {i+1}",
                department="Sales",
                employee_id=f"emp_sales_quote_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Quotation Specialist", "emp_sales_quote_001", "Quotation creation and follow-up")

        # Sales Order Team Lead
        order_lead = self.bridge.create_operations_employee(
            employee_name="عبدالرحمن الطلبات",  # Abdulrahman Al-Talabat
            department="Sales",
            employee_id="emp_sales_order_001"
        )
        self._register_employee(order_lead, "Sales Order Team Lead", "emp_sales_dir_001", "Sales order processing")

        # Sales Order Specialists
        for i in range(5):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص الطلبات {i+1}",
                department="Sales",
                employee_id=f"emp_sales_order_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Sales Order Specialist", "emp_sales_order_001", "Order fulfillment")

        # Sales Invoice Team Lead
        invoice_lead = self.bridge.create_operations_employee(
            employee_name="هند الفواتير",  # Hind Al-Fawateer
            department="Sales",
            employee_id="emp_sales_inv_001"
        )
        self._register_employee(invoice_lead, "Sales Invoice Team Lead", "emp_sales_dir_001", "Sales invoicing")

        # Sales Invoice Specialists
        for i in range(3):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص الفواتير {i+1}",
                department="Sales",
                employee_id=f"emp_sales_inv_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Invoice Specialist", "emp_sales_inv_001", "Invoice generation and tracking")

        # Sales Analyst
        analyst = self.bridge.create_explorer_employee(
            employee_name="سلطان التحليل",  # Sultan Al-Tahlil
            department="Sales",
            employee_id="emp_sales_analyst_001"
        )
        self._register_employee(analyst, "Sales Analyst", "emp_sales_dir_001", "Sales performance analysis")

        self._create_org_unit("Sales", "Sales Management", "Sales",
                             "emp_sales_dir_001",
                             ["emp_sales_quote_001", "emp_sales_order_001", "emp_sales_inv_001"],
                             ["emp_sales_analyst_001"])

    def _create_buying_department(self):
        """Create Procurement/Buying department"""
        logger.info("Creating Procurement department...")

        # Procurement Director
        director = self.bridge.create_planner_employee(
            employee_name="طارق المشتريات",  # Tariq Al-Mushtarayat
            department="Procurement",
            employee_id="emp_buy_dir_001"
        )
        self._register_employee(director, "Procurement Director", "emp_coo_001", "Procurement strategy")

        # Supplier Management Lead
        supplier_lead = self.bridge.create_operations_employee(
            employee_name="منى الموردين",  # Muna Al-Muwarrideen
            department="Procurement",
            employee_id="emp_buy_supp_001"
        )
        self._register_employee(supplier_lead, "Supplier Management Lead", "emp_buy_dir_001", "Supplier relationships")

        # Purchase Order Team Lead
        po_lead = self.bridge.create_operations_employee(
            employee_name="وليد الطلبات",  # Waleed Al-Talabat
            department="Procurement",
            employee_id="emp_buy_po_001"
        )
        self._register_employee(po_lead, "Purchase Order Team Lead", "emp_buy_dir_001", "Purchase order management")

        # Purchase Specialists
        for i in range(4):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص المشتريات {i+1}",
                department="Procurement",
                employee_id=f"emp_buy_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Purchase Specialist", "emp_buy_po_001", "Purchase processing")

        # Procurement Analyst
        analyst = self.bridge.create_explorer_employee(
            employee_name="عائشة التحليل",  # Aisha Al-Tahlil
            department="Procurement",
            employee_id="emp_buy_analyst_001"
        )
        self._register_employee(analyst, "Procurement Analyst", "emp_buy_dir_001", "Spend analysis and optimization")

        self._create_org_unit("Procurement", "Procurement Management", "Buying",
                             "emp_buy_dir_001",
                             ["emp_buy_supp_001", "emp_buy_po_001"],
                             ["emp_buy_analyst_001"])

    def _create_inventory_department(self):
        """Create Inventory/Stock department"""
        logger.info("Creating Inventory department...")

        # Inventory Director
        director = self.bridge.create_planner_employee(
            employee_name="راشد المخزون",  # Rashed Al-Makhzoon
            department="Inventory",
            employee_id="emp_inv_dir_001"
        )
        self._register_employee(director, "Inventory Director", "emp_coo_001", "Inventory strategy and optimization")

        # Warehouse Management Lead
        warehouse_lead = self.bridge.create_operations_employee(
            employee_name="لطيفة المستودعات",  # Latifa Al-Mustawda'at
            department="Inventory",
            employee_id="emp_inv_wh_001"
        )
        self._register_employee(warehouse_lead, "Warehouse Management Lead", "emp_inv_dir_001", "Warehouse operations")

        # Warehouse Specialists
        for i in range(5):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص المستودعات {i+1}",
                department="Inventory",
                employee_id=f"emp_inv_wh_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Warehouse Specialist", "emp_inv_wh_001", "Stock management")

        # Item Master Lead
        item_lead = self.bridge.create_operations_employee(
            employee_name="بدر الأصناف",  # Badr Al-Asnaf
            department="Inventory",
            employee_id="emp_inv_item_001"
        )
        self._register_employee(item_lead, "Item Master Lead", "emp_inv_dir_001", "Item data management")

        # Stock Control Lead
        stock_lead = self.bridge.create_operations_employee(
            employee_name="جواهر الجرد",  # Jawaher Al-Jard
            department="Inventory",
            employee_id="emp_inv_stock_001"
        )
        self._register_employee(stock_lead, "Stock Control Lead", "emp_inv_dir_001", "Stock reconciliation")

        # Inventory Analyst
        analyst = self.bridge.create_explorer_employee(
            employee_name="فهد التحليل",  # Fahad Al-Tahlil
            department="Inventory",
            employee_id="emp_inv_analyst_001"
        )
        self._register_employee(analyst, "Inventory Analyst", "emp_inv_dir_001", "Stock level analysis and forecasting")

        self._create_org_unit("Inventory", "Inventory Management", "Stock",
                             "emp_inv_dir_001",
                             ["emp_inv_wh_001", "emp_inv_item_001", "emp_inv_stock_001"],
                             ["emp_inv_analyst_001"])

    def _create_accounting_department(self):
        """Create Accounting/Finance department"""
        logger.info("Creating Accounting department...")

        # Finance Director (reports to CFO)
        director = self.bridge.create_planner_employee(
            employee_name="سعد المحاسبة",  # Saad Al-Muhasaba
            department="Finance",
            employee_id="emp_acc_dir_001"
        )
        self._register_employee(director, "Finance Director", "emp_cfo_001", "Financial operations")

        # Accounts Receivable Lead
        ar_lead = self.bridge.create_operations_employee(
            employee_name="غادة المدينين",  # Ghada Al-Madyooneen
            department="Finance",
            employee_id="emp_acc_ar_001"
        )
        self._register_employee(ar_lead, "Accounts Receivable Lead", "emp_acc_dir_001", "Customer payments")

        # Accounts Payable Lead
        ap_lead = self.bridge.create_operations_employee(
            employee_name="ماجد الدائنين",  # Majed Al-Da'ineen
            department="Finance",
            employee_id="emp_acc_ap_001"
        )
        self._register_employee(ap_lead, "Accounts Payable Lead", "emp_acc_dir_001", "Supplier payments")

        # General Ledger Lead
        gl_lead = self.bridge.create_operations_employee(
            employee_name="أمل الأستاذ",  # Amal Al-Ustaz
            department="Finance",
            employee_id="emp_acc_gl_001"
        )
        self._register_employee(gl_lead, "General Ledger Lead", "emp_acc_dir_001", "GL entries and reconciliation")

        # Financial Accountants
        for i in range(4):
            accountant = self.bridge.create_operations_employee(
                employee_name=f"محاسب {i+1}",
                department="Finance",
                employee_id=f"emp_acc_spec_{i+1:03d}"
            )
            self._register_employee(accountant, "Financial Accountant", "emp_acc_gl_001", "Journal entries and reporting")

        # Financial Analyst
        analyst = self.bridge.create_explorer_employee(
            employee_name="عمر التحليل المالي",  # Omar Al-Tahlil Al-Mali
            department="Finance",
            employee_id="emp_acc_analyst_001"
        )
        self._register_employee(analyst, "Financial Analyst", "emp_acc_dir_001", "Financial analysis and reporting")

        self._create_org_unit("Finance", "Financial Accounting", "Accounts",
                             "emp_acc_dir_001",
                             ["emp_acc_ar_001", "emp_acc_ap_001", "emp_acc_gl_001"],
                             ["emp_acc_analyst_001"])

    def _create_hr_department(self):
        """Create Human Resources department"""
        logger.info("Creating HR department...")

        # HR Director
        director = self.bridge.create_planner_employee(
            employee_name="ليلى الموارد",  # Laila Al-Mawarid
            department="HR",
            employee_id="emp_hr_dir_001"
        )
        self._register_employee(director, "HR Director", "emp_ceo_001", "Human resources strategy")

        # Recruitment Lead
        recruit_lead = self.bridge.create_operations_employee(
            employee_name="إبراهيم التوظيف",  # Ibrahim Al-Tawtheef
            department="HR",
            employee_id="emp_hr_recruit_001"
        )
        self._register_employee(recruit_lead, "Recruitment Lead", "emp_hr_dir_001", "Talent acquisition")

        # Payroll Lead
        payroll_lead = self.bridge.create_operations_employee(
            employee_name="رنا الرواتب",  # Rana Al-Rawatib
            department="HR",
            employee_id="emp_hr_payroll_001"
        )
        self._register_employee(payroll_lead, "Payroll Lead", "emp_hr_dir_001", "Payroll processing")

        # Attendance & Leave Lead
        attendance_lead = self.bridge.create_operations_employee(
            employee_name="زياد الحضور",  # Ziyad Al-Hudoor
            department="HR",
            employee_id="emp_hr_attend_001"
        )
        self._register_employee(attendance_lead, "Attendance & Leave Lead", "emp_hr_dir_001", "Attendance tracking")

        # HR Specialists
        for i in range(3):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص الموارد {i+1}",
                department="HR",
                employee_id=f"emp_hr_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "HR Specialist", "emp_hr_dir_001", "Employee services")

        self._create_org_unit("HR", "Human Resources", "HR",
                             "emp_hr_dir_001",
                             ["emp_hr_recruit_001", "emp_hr_payroll_001", "emp_hr_attend_001"],
                             [])

    def _create_projects_department(self):
        """Create Projects department"""
        logger.info("Creating Projects department...")

        # PMO Director
        director = self.bridge.create_planner_employee(
            employee_name="حسن المشاريع",  # Hassan Al-Masharee
            department="PMO",
            employee_id="emp_pm_dir_001"
        )
        self._register_employee(director, "PMO Director", "emp_coo_001", "Project portfolio management")

        # Project Managers
        for i in range(3):
            pm = self.bridge.create_planner_employee(
                employee_name=f"مدير مشروع {i+1}",
                department="PMO",
                employee_id=f"emp_pm_{i+1:03d}"
            )
            self._register_employee(pm, "Project Manager", "emp_pm_dir_001", "Project execution")

        # Timesheet Coordinator
        timesheet_coord = self.bridge.create_operations_employee(
            employee_name="دانة الساعات",  # Dana Al-Sa'at
            department="PMO",
            employee_id="emp_pm_time_001"
        )
        self._register_employee(timesheet_coord, "Timesheet Coordinator", "emp_pm_dir_001", "Time tracking")

        self._create_org_unit("PMO", "Project Management Office", "Projects",
                             "emp_pm_dir_001",
                             [f"emp_pm_{i+1:03d}" for i in range(3)],
                             ["emp_pm_time_001"])

    def _create_manufacturing_department(self):
        """Create Manufacturing department"""
        logger.info("Creating Manufacturing department...")

        # Manufacturing Director
        director = self.bridge.create_planner_employee(
            employee_name="صالح الإنتاج",  # Saleh Al-Intaj
            department="Manufacturing",
            employee_id="emp_mfg_dir_001"
        )
        self._register_employee(director, "Manufacturing Director", "emp_coo_001", "Production planning")

        # Production Planning Lead
        planning_lead = self.bridge.create_planner_employee(
            employee_name="شيخة التخطيط",  # Sheikha Al-Takhteet
            department="Manufacturing",
            employee_id="emp_mfg_plan_001"
        )
        self._register_employee(planning_lead, "Production Planning Lead", "emp_mfg_dir_001", "Production scheduling")

        # Work Order Lead
        wo_lead = self.bridge.create_operations_employee(
            employee_name="عادل أوامر العمل",  # Adel Awamir Al-Amal
            department="Manufacturing",
            employee_id="emp_mfg_wo_001"
        )
        self._register_employee(wo_lead, "Work Order Lead", "emp_mfg_dir_001", "Work order management")

        # BOM Engineer
        bom_eng = self.bridge.create_explorer_employee(
            employee_name="مهند الهيكل",  # Muhannad Al-Haikal
            department="Manufacturing",
            employee_id="emp_mfg_bom_001"
        )
        self._register_employee(bom_eng, "BOM Engineer", "emp_mfg_dir_001", "Bill of materials management")

        self._create_org_unit("Manufacturing", "Production Management", "Manufacturing",
                             "emp_mfg_dir_001",
                             ["emp_mfg_plan_001", "emp_mfg_wo_001"],
                             ["emp_mfg_bom_001"])

    def _create_support_department(self):
        """Create Customer Support department"""
        logger.info("Creating Support department...")

        # Support Director
        director = self.bridge.create_planner_employee(
            employee_name="جميلة الدعم",  # Jameela Al-Daem
            department="Support",
            employee_id="emp_sup_dir_001"
        )
        self._register_employee(director, "Support Director", "emp_coo_001", "Customer support strategy")

        # Support Team Lead
        team_lead = self.bridge.create_operations_employee(
            employee_name="يوسف الخدمة",  # Youssef Al-Khidma
            department="Support",
            employee_id="emp_sup_lead_001"
        )
        self._register_employee(team_lead, "Support Team Lead", "emp_sup_dir_001", "Support ticket management")

        # Support Specialists
        for i in range(5):
            specialist = self.bridge.create_operations_employee(
                employee_name=f"متخصص الدعم {i+1}",
                department="Support",
                employee_id=f"emp_sup_spec_{i+1:03d}"
            )
            self._register_employee(specialist, "Support Specialist", "emp_sup_lead_001", "Customer issue resolution")

        self._create_org_unit("Support", "Customer Support", "Support",
                             "emp_sup_dir_001",
                             ["emp_sup_lead_001"],
                             [])

    def _create_quality_department(self):
        """Create Quality Management department"""
        logger.info("Creating Quality department...")

        # Quality Director
        director = self.bridge.create_planner_employee(
            employee_name="نايف الجودة",  # Nayef Al-Jawda
            department="Quality",
            employee_id="emp_qc_dir_001"
        )
        self._register_employee(director, "Quality Director", "emp_coo_001", "Quality assurance strategy")

        # Quality Inspector Lead
        inspector_lead = self.bridge.create_operations_employee(
            employee_name="أسماء التفتيش",  # Asma Al-Tafteesh
            department="Quality",
            employee_id="emp_qc_insp_001"
        )
        self._register_employee(inspector_lead, "Quality Inspector Lead", "emp_qc_dir_001", "Quality inspections")

        # Quality Inspectors
        for i in range(3):
            inspector = self.bridge.create_operations_employee(
                employee_name=f"مفتش الجودة {i+1}",
                department="Quality",
                employee_id=f"emp_qc_insp_{i+1:03d}"
            )
            self._register_employee(inspector, "Quality Inspector", "emp_qc_insp_001", "Quality checks")

        self._create_org_unit("Quality", "Quality Management", "Quality",
                             "emp_qc_dir_001",
                             ["emp_qc_insp_001"],
                             [])

    def _create_assets_department(self):
        """Create Asset Management department"""
        logger.info("Creating Assets department...")

        # Assets Director
        director = self.bridge.create_planner_employee(
            employee_name="فيصل الأصول",  # Faisal Al-Usool
            department="Assets",
            employee_id="emp_asset_dir_001"
        )
        self._register_employee(director, "Assets Director", "emp_cfo_001", "Asset management strategy")

        # Asset Maintenance Lead
        maint_lead = self.bridge.create_operations_employee(
            employee_name="وفاء الصيانة",  # Wafa Al-Siyana
            department="Assets",
            employee_id="emp_asset_maint_001"
        )
        self._register_employee(maint_lead, "Asset Maintenance Lead", "emp_asset_dir_001", "Preventive maintenance")

        # Asset Custodian
        custodian = self.bridge.create_operations_employee(
            employee_name="تركي الحفظ",  # Turki Al-Hifth
            department="Assets",
            employee_id="emp_asset_cust_001"
        )
        self._register_employee(custodian, "Asset Custodian", "emp_asset_dir_001", "Asset tracking")

        self._create_org_unit("Assets", "Asset Management", "Assets",
                             "emp_asset_dir_001",
                             ["emp_asset_maint_001"],
                             ["emp_asset_cust_001"])

    def _create_it_department(self):
        """Create IT Operations department"""
        logger.info("Creating IT department...")

        # IT Director (reports to CTO)
        director = self.bridge.create_explorer_employee(
            employee_name="علي التقنية",  # Ali Al-Tiqniya
            department="IT",
            employee_id="emp_it_dir_001"
        )
        self._register_employee(director, "IT Director", "emp_cto_001", "IT operations and system administration")

        # System Administrator
        sysadmin = self.bridge.create_explorer_employee(
            employee_name="منار الأنظمة",  # Manar Al-Andhima
            department="IT",
            employee_id="emp_it_admin_001"
        )
        self._register_employee(sysadmin, "System Administrator", "emp_it_dir_001", "ERPNext administration")

        # Customization Developer
        dev = self.bridge.create_planner_employee(
            employee_name="عبدالعزيز التطوير",  # Abdulaziz Al-Tatweer
            department="IT",
            employee_id="emp_it_dev_001"
        )
        self._register_employee(dev, "Customization Developer", "emp_it_dir_001", "Custom development")

        # Data Analyst
        analyst = self.bridge.create_explorer_employee(
            employee_name="حنان البيانات",  # Hanan Al-Bayanat
            department="IT",
            employee_id="emp_it_analyst_001"
        )
        self._register_employee(analyst, "Data Analyst", "emp_it_dir_001", "Data analysis and reporting")

        self._create_org_unit("IT", "Information Technology", "IT",
                             "emp_it_dir_001",
                             ["emp_it_admin_001", "emp_it_dev_001"],
                             ["emp_it_analyst_001"])

    def _register_employee(self, employee: SubagentEmployee, title: str,
                          manager_id: Optional[str], responsibilities: str):
        """Register an employee in the registry"""
        self.employee_registry[employee.employee_id] = {
            "employee": employee,
            "title": title,
            "manager_id": manager_id,
            "responsibilities": responsibilities,
            "direct_reports": []
        }

        # Update manager's direct reports
        if manager_id and manager_id in self.employee_registry:
            self.employee_registry[manager_id]["direct_reports"].append(employee.employee_id)

    def _create_org_unit(self, unit_id: str, name: str, module: str,
                        manager_id: str, team_leads: List[str], specialists: List[str]):
        """Create an organizational unit"""
        self.org_units[unit_id] = OrganizationalUnit(
            unit_id=unit_id,
            name=name,
            module=module,
            description=self.modules.get(module, {}).get("name", ""),
            manager_id=manager_id,
            team_leads=team_leads,
            specialists=specialists
        )

    def get_org_chart_summary(self) -> Dict:
        """Get organizational chart summary"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_employees": len(self.employee_registry),
            "total_departments": len(self.org_units),
            "by_department": {},
            "by_role_type": {
                "executives": 0,
                "directors": 0,
                "managers": 0,
                "specialists": 0,
                "analysts": 0
            },
            "by_subagent_type": {
                "Explore": 0,
                "Plan": 0,
                "general-purpose": 0
            }
        }

        for emp_id, emp_data in self.employee_registry.items():
            employee = emp_data["employee"]
            title = emp_data["title"]

            # Count by department
            dept = employee.department
            if dept not in summary["by_department"]:
                summary["by_department"][dept] = 0
            summary["by_department"][dept] += 1

            # Count by role type
            if "CEO" in title or "CFO" in title or "CTO" in title or "COO" in title:
                summary["by_role_type"]["executives"] += 1
            elif "Director" in title:
                summary["by_role_type"]["directors"] += 1
            elif "Lead" in title or "Manager" in title:
                summary["by_role_type"]["managers"] += 1
            elif "Analyst" in title:
                summary["by_role_type"]["analysts"] += 1
            else:
                summary["by_role_type"]["specialists"] += 1

            # Count by subagent type
            summary["by_subagent_type"][employee.subagent_type] += 1

        return summary

    def generate_org_chart_text(self) -> str:
        """Generate text-based organizational chart"""
        lines = []
        lines.append("="*80)
        lines.append("ERPNEXT COMPLETE ORGANIZATIONAL CHART")
        lines.append("="*80)
        lines.append("")

        # Start with CEO
        ceo_id = "emp_ceo_001"
        if ceo_id in self.employee_registry:
            self._append_employee_tree(lines, ceo_id, 0)

        return "\n".join(lines)

    def _append_employee_tree(self, lines: List[str], emp_id: str, level: int):
        """Recursively append employee tree"""
        if emp_id not in self.employee_registry:
            return

        emp_data = self.employee_registry[emp_id]
        employee = emp_data["employee"]
        title = emp_data["title"]

        indent = "  " * level
        prefix = "└─ " if level > 0 else ""

        lines.append(f"{indent}{prefix}{employee.employee_name}")
        lines.append(f"{indent}   {title} | {employee.department}")
        lines.append(f"{indent}   Type: {employee.subagent_type}")

        # Add direct reports
        for report_id in emp_data["direct_reports"]:
            self._append_employee_tree(lines, report_id, level + 1)

        if level == 0:
            lines.append("")

    def save_org_chart(self, filename: str = "erpnext_org_chart.json"):
        """Save organizational chart to file"""
        data = {
            "created_at": datetime.now().isoformat(),
            "summary": self.get_org_chart_summary(),
            "org_units": {uid: asdict(unit) for uid, unit in self.org_units.items()},
            "employees": {
                emp_id: {
                    "name": emp_data["employee"].employee_name,
                    "title": emp_data["title"],
                    "department": emp_data["employee"].department,
                    "role": emp_data["employee"].role,
                    "subagent_type": emp_data["employee"].subagent_type,
                    "manager_id": emp_data["manager_id"],
                    "responsibilities": emp_data["responsibilities"],
                    "direct_reports": emp_data["direct_reports"]
                }
                for emp_id, emp_data in self.employee_registry.items()
            }
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Organizational chart saved to {filename}")


# Example usage
if __name__ == "__main__":
    from claude_code_bridge import SubagentERPNextBridge
    import os

    print("\n" + "="*80)
    print("CREATING COMPLETE ERPNEXT ORGANIZATIONAL CHART")
    print("="*80 + "\n")

    # Initialize bridge
    bridge = SubagentERPNextBridge(
        erpnext_base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    )

    # Create org chart
    org_chart = ERPNextOrgChart(bridge)
    summary = org_chart.create_complete_org_chart()

    # Display summary
    print("\nORGANIZATIONAL SUMMARY:")
    print("-" * 80)
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    # Display text org chart
    print("\n" + org_chart.generate_org_chart_text())

    # Save to file
    org_chart.save_org_chart("erpnext_complete_org_chart.json")
    bridge.save_state("org_chart_employees_state.json")

    print("\n" + "="*80)
    print("ORG CHART CREATION COMPLETE!")
    print("="*80)
    print(f"\nTotal Employees: {summary['total_employees']}")
    print(f"Total Departments: {summary['total_departments']}")
    print("\nFiles created:")
    print("  - erpnext_complete_org_chart.json")
    print("  - org_chart_employees_state.json")
    print("\n" + "="*80)
