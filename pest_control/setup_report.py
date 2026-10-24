import frappe

def create_report():
    if not frappe.db.exists("Report", "Daily Manpower Deployment"):
        rep = frappe.get_doc({
            "doctype": "Report",
            "report_name": "Daily Manpower Deployment",
            "ref_doctype": "Manpower Allocation",
            "report_type": "Report Builder",
            "module": "Pest Control",
            "is_standard": "Yes",
            "json": """[
                {"fieldname": "allocation_date", "label": "Date", "fieldtype": "Date", "width": 120},
                {"fieldname": "time_slot", "label": "Shift / Slot", "fieldtype": "Select", "width": 160},
                {"fieldname": "employee_name", "label": "Technician", "fieldtype": "Data", "width": 160},
                {"fieldname": "role", "label": "Role", "fieldtype": "Select", "width": 140},
                {"fieldname": "work_order", "label": "Work Order", "fieldtype": "Link", "width": 140},
                {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "width": 160},
                {"fieldname": "site", "label": "Site Facility", "fieldtype": "Link", "width": 200},
                {"fieldname": "service_type", "label": "Service", "fieldtype": "Link", "width": 180},
                {"fieldname": "status", "label": "Status", "fieldtype": "Select", "width": 120}
            ]"""
        })
        rep.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created Daily Manpower Deployment Report!")
    else:
        print("Report already exists.")