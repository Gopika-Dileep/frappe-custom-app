import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_custom_fields():
    print("Setting up Custom Fields on Employee for Pest Control Manpower...")
    custom_fields = {
        "Employee": [
            {
                "fieldname": "pest_control_section",
                "label": "Pest Control & FM Skills",
                "fieldtype": "Section Break",
                "insert_after": "status"
            },
            {
                "fieldname": "is_pest_technician",
                "label": "Available for Pest Service Allocation",
                "fieldtype": "Check",
                "default": 1,
                "insert_after": "pest_control_section"
            },
            {
                "fieldname": "technician_certification",
                "label": "Pest Certification / Skill Level",
                "fieldtype": "Select",
                "options": "Licensed Pest Technician\nFumigation & Termite Specialist\nRodent & Vector Control Specialist\nTrainee / Assistant Technician",
                "default": "Licensed Pest Technician",
                "insert_after": "is_pest_technician"
            },
            {
                "fieldname": "pesticide_license_no",
                "label": "Pesticide Operator License No",
                "fieldtype": "Data",
                "insert_after": "technician_certification"
            },
            {
                "fieldname": "license_expiry_date",
                "label": "License Expiry Date",
                "fieldtype": "Date",
                "insert_after": "pesticide_license_no"
            }
        ]
    }
    create_custom_fields(custom_fields, update=True)
    frappe.db.commit()
    print("Custom Fields on Employee created successfully!")