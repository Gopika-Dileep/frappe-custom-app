import frappe
from hrms.utils import get_employee_email

def run():
    emp = frappe.get_doc("Employee", "HR-EMP-00007")
    print("prefered_email:", emp.prefered_email)
    print("user_id:", emp.user_id)
    print("company_email:", emp.company_email)
    print("personal_email:", emp.personal_email)
    print("Resolved email from get_employee_email:", get_employee_email("HR-EMP-00007"))
    
    # Check notifications or communication logs for HR-LAP-2026-00005
    comms = frappe.get_all("Communication", filters={"reference_doctype": "Leave Application", "reference_name": "HR-LAP-2026-00005"}, fields=["name", "sender", "recipients", "subject", "content"])
    print("\n--- COMMUNICATIONS FOR HR-LAP-2026-00005 ---")
    for c in comms:
        print(c)

    # Check Activity / Comments / Version
    comments = frappe.get_all("Comment", filters={"reference_doctype": "Leave Application", "reference_name": "HR-LAP-2026-00005"}, fields=["name", "comment_type", "comment_by", "content"])
    print("\n--- COMMENTS / TIMELINE FOR HR-LAP-2026-00005 ---")
    for cm in comments:
        print(cm)
