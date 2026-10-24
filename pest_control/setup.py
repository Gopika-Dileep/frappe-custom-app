import frappe

def create_doctypes():
    print("Continuing DocType setup for Pest Control Manpower Management...")

    # 1. Child Table: Pest Work Order Technician (manpower_allocation as Data initially)
    if not frappe.db.exists("DocType", "Pest Work Order Technician"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Pest Work Order Technician",
            "module": "Pest Control",
            "custom": 0,
            "istable": 1,
            "fields": [
                {"fieldname": "employee", "label": "Technician (Employee)", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "employee_name", "label": "Technician Name", "fieldtype": "Data", "fetch_from": "employee.employee_name", "read_only": 1, "in_list_view": 1},
                {"fieldname": "role", "label": "Role", "fieldtype": "Select", "options": "Lead Technician\nAssistant Technician\nChemical Sprayer\nQuality Inspector", "default": "Lead Technician", "in_list_view": 1},
                {"fieldname": "contact_number", "label": "Contact Number", "fieldtype": "Data", "fetch_from": "employee.cell_number", "read_only": 1, "in_list_view": 1},
                {"fieldname": "manpower_allocation", "label": "Allocation Reference", "fieldtype": "Data", "read_only": 1}
            ]
        })
        doc.insert()
        frappe.db.commit()
        print("Created Pest Work Order Technician child table")

    # 2. Operational: Pest Work Order
    if not frappe.db.exists("DocType", "Pest Work Order"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Pest Work Order",
            "module": "Pest Control",
            "custom": 0,
            "istable": 0,
            "is_submittable": 1,
            "autoname": "naming_series:",
            "fields": [
                {"fieldname": "naming_series", "label": "Series", "fieldtype": "Select", "options": "PWO-.YYYY.-", "default": "PWO-.YYYY.-", "reqd": 1},
                {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "reqd": 1, "in_list_view": 1},
                {"fieldname": "customer_name", "label": "Customer Name", "fieldtype": "Data", "fetch_from": "customer.customer_name", "read_only": 1},
                {"fieldname": "site", "label": "Service Site", "fieldtype": "Link", "options": "Pest Control Site", "reqd": 1, "in_list_view": 1},
                {"fieldname": "contract", "label": "Contract (AMC)", "fieldtype": "Link", "options": "Pest Control Contract"},
                {"fieldname": "service_type", "label": "Service Type", "fieldtype": "Link", "options": "Service Type", "reqd": 1, "in_list_view": 1},
                {"fieldname": "scheduled_date", "label": "Scheduled Date", "fieldtype": "Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "time_slot", "label": "Time Slot / Shift", "fieldtype": "Select", "options": "Morning (08:00 - 12:00)\nAfternoon (13:00 - 17:00)\nEvening/Night (18:00 - 22:00)", "default": "Morning (08:00 - 12:00)", "reqd": 1, "in_list_view": 1},
                {"fieldname": "priority", "label": "Priority", "fieldtype": "Select", "options": "Standard\nHigh\nUrgent / Emergency Infestation", "default": "Standard", "in_list_view": 1},
                {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Draft\nScheduled\nIn Progress\nCompleted\nCancelled", "default": "Draft", "in_list_view": 1},
                {"fieldname": "manpower_section", "label": "Manpower Allocation", "fieldtype": "Section Break"},
                {"fieldname": "allocated_technicians", "label": "Assigned Technicians", "fieldtype": "Table", "options": "Pest Work Order Technician"},
                {"fieldname": "chemicals_section", "label": "Chemicals & Treatments Applied", "fieldtype": "Section Break"},
                {"fieldname": "chemicals_used", "label": "Chemicals Used", "fieldtype": "Table", "options": "Pest Chemical Consumable"},
                {"fieldname": "completion_section", "label": "Service Closure & Sign-off", "fieldtype": "Section Break"},
                {"fieldname": "completion_date", "label": "Completion Date", "fieldtype": "Date"},
                {"fieldname": "client_feedback", "label": "Client Feedback", "fieldtype": "Select", "options": "Pending\nExcellent\nGood\nSatisfactory\nUnsatisfactory", "default": "Pending"},
                {"fieldname": "technician_remarks", "label": "Technician Observations", "fieldtype": "Small Text"},
                {"fieldname": "supervisor_notes", "label": "Supervisor Quality Notes", "fieldtype": "Small Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1}]
        })
        doc.insert()
        frappe.db.commit()
        print("Created Pest Work Order")

    # 3. Star: Manpower Allocation
    if not frappe.db.exists("DocType", "Manpower Allocation"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Manpower Allocation",
            "module": "Pest Control",
            "custom": 0,
            "istable": 0,
            "is_submittable": 1,
            "autoname": "naming_series:",
            "fields": [
                {"fieldname": "naming_series", "label": "Series", "fieldtype": "Select", "options": "MPA-.YYYY.-", "default": "MPA-.YYYY.-", "reqd": 1},
                {"fieldname": "work_order", "label": "Pest Work Order", "fieldtype": "Link", "options": "Pest Work Order", "reqd": 1, "in_list_view": 1},
                {"fieldname": "employee", "label": "Field Technician (Employee)", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "employee_name", "label": "Technician Name", "fieldtype": "Data", "fetch_from": "employee.employee_name", "read_only": 1, "in_list_view": 1},
                {"fieldname": "customer", "label": "Customer", "fieldtype": "Link", "options": "Customer", "fetch_from": "work_order.customer", "read_only": 1},
                {"fieldname": "site", "label": "Site / Facility", "fieldtype": "Link", "options": "Pest Control Site", "fetch_from": "work_order.site", "read_only": 1, "in_list_view": 1},
                {"fieldname": "service_type", "label": "Service Type", "fieldtype": "Link", "options": "Service Type", "fetch_from": "work_order.service_type", "read_only": 1},
                {"fieldname": "allocation_date", "label": "Allocation Date", "fieldtype": "Date", "fetch_from": "work_order.scheduled_date", "read_only": 1, "in_list_view": 1},
                {"fieldname": "time_slot", "label": "Time Slot / Shift", "fieldtype": "Select", "options": "Morning (08:00 - 12:00)\nAfternoon (13:00 - 17:00)\nEvening/Night (18:00 - 22:00)", "fetch_from": "work_order.time_slot", "read_only": 1, "in_list_view": 1},
                {"fieldname": "role", "label": "Deployment Role", "fieldtype": "Select", "options": "Lead Technician\nAssistant Technician\nChemical Sprayer\nQuality Inspector", "default": "Lead Technician", "in_list_view": 1},
                {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Assigned\nDispatched\nOn Site\nCompleted\nAbsent / Reassigned", "default": "Assigned", "in_list_view": 1},
                {"fieldname": "checkin_time", "label": "Site Arrival (Checkin)", "fieldtype": "Datetime"},
                {"fieldname": "checkout_time", "label": "Site Departure (Checkout)", "fieldtype": "Datetime"},
                {"fieldname": "notes", "label": "Allocation Notes", "fieldtype": "Small Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "amend": 1}]
        })
        doc.insert()
        frappe.db.commit()
        print("Created Manpower Allocation")

    # 4. Update Pest Work Order Technician to Link to Manpower Allocation
    pwot = frappe.get_doc("DocType", "Pest Work Order Technician")
    for field in pwot.fields:
        if field.fieldname == "manpower_allocation":
            field.fieldtype = "Link"
            field.options = "Manpower Allocation"
            pwot.save()
            frappe.db.commit()
            print("Updated Pest Work Order Technician link to Manpower Allocation")
            break

    print("ALL DocTypes successfully initialized!")