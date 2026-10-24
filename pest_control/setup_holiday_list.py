import frappe
from frappe.utils import today

def setup():
    company = frappe.get_all("Company")[0].name
    hl_name = f"{company} Holiday List 2026"
    if not frappe.db.exists("Holiday List", hl_name):
        hl = frappe.get_doc({
            "doctype": "Holiday List",
            "holiday_list_name": hl_name,
            "from_date": "2026-01-01",
            "to_date": "2026-12-31",
            "weekly_off": "Sunday"
        })
        hl.get_weekly_off_dates()
        hl.insert(ignore_permissions=True)
        print("Created Holiday List:", hl_name)

    # Set as default for Company
    frappe.db.set_value("Company", company, "default_holiday_list", hl_name)
    frappe.db.commit()
    print("Assigned default holiday list to Company", company)