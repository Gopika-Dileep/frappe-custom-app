import frappe

def create_workspace():
    if not frappe.db.exists("Workspace", "Pest Control"):
        ws = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Pest Control",
            "label": "Pest Control",
            "title": "Pest Control & FM",
            "icon": "shield",
            "module": "Pest Control",
            "is_standard": 1,
            "public": 1,
            "roles": [{"role": "System Manager"}],
            "shortcuts": [
                {"type": "DocType", "link_to": "Pest Work Order", "label": "Work Orders"},
                {"type": "DocType", "link_to": "Manpower Allocation", "label": "Manpower Allocation"},
                {"type": "DocType", "link_to": "Pest Control Contract", "label": "Service Contracts"},
                {"type": "DocType", "link_to": "Pest Control Site", "label": "Client Sites"},
                {"type": "DocType", "link_to": "Service Type", "label": "Service Types"}
            ],
            "links": [
                {"label": "Operations", "type": "Card Break"},
                {"type": "Link", "link_type": "DocType", "link_to": "Pest Work Order", "label": "Pest Work Order"},
                {"type": "Link", "link_type": "DocType", "link_to": "Manpower Allocation", "label": "Manpower Allocation"},
                {"type": "Link", "link_type": "DocType", "link_to": "Pest Control Site", "label": "Pest Control Site"},
                {"label": "Contracts & CRM", "type": "Card Break"},
                {"type": "Link", "link_type": "DocType", "link_to": "Pest Control Contract", "label": "Pest Control Contract"},
                {"type": "Link", "link_type": "DocType", "link_to": "Customer", "label": "Customers (ERPNext)"},
                {"label": "HR & Manpower Masters", "type": "Card Break"},
                {"type": "Link", "link_type": "DocType", "link_to": "Employee", "label": "Field Technicians (Frappe HR)"},
                {"type": "Link", "link_type": "DocType", "link_to": "Leave Application", "label": "Leave Applications (Frappe HR)"},
                {"type": "Link", "link_type": "DocType", "link_to": "Service Type", "label": "Service Types"}
            ]
        })
        ws.insert()
        frappe.db.commit()
        print("Created Pest Control Workspace!")
    else:
        print("Pest Control Workspace already exists.")