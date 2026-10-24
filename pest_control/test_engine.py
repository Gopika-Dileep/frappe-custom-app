import frappe
from frappe.utils import today
from pest_control.api import get_available_technicians

def run_test():
    print("\n--- TEST 1: Smart Availability Query ---")
    available = get_available_technicians(today(), "Morning (08:00 - 12:00)")
    names = [t["employee_name"] for t in available]
    print(f"Available technicians for today morning slot: {names}")

    # Rahul should NOT be here (already booked)
    # Asif should NOT be here (on approved leave)
    # Akhil, Vineeth, Shaiju should be available!
    print("Rahul Menon in available? (Should be False):", "Rahul Menon" in names)
    print("Muhammed Asif in available? (Should be False):", "Muhammed Asif" in names)
    print("Akhil Raj in available? (Should be True):", "Akhil Raj" in names)

    print("\n--- TEST 2: Double-Booking Prevention Rule ---")
    rahul_id = frappe.db.get_value("Employee", {"employee_name": "Rahul Menon"}, "name")
    try:
        alloc_dup = frappe.get_doc({
            "doctype": "Manpower Allocation",
            "work_order": "PWO-2026-00002",
            "employee": rahul_id,
            "role": "Lead Technician",
            "status": "Assigned"
        })
        alloc_dup.insert()
        print("FAIL: Double booking was allowed!")
    except Exception as e:
        print("SUCCESS! Double booking was blocked correctly with message:")
        print("  ->", str(e))

    print("\n--- TEST 3: Approved Leave Conflict Rule ---")
    asif_id = frappe.db.get_value("Employee", {"employee_name": "Muhammed Asif"}, "name")
    try:
        alloc_leave = frappe.get_doc({
            "doctype": "Manpower Allocation",
            "work_order": "PWO-2026-00002",
            "employee": asif_id,
            "role": "Lead Technician",
            "status": "Assigned"
        })
        alloc_leave.insert()
        print("FAIL: Leave conflict was allowed!")
    except Exception as e:
        print("SUCCESS! Leave conflict was blocked correctly with message:")
        print("  ->", str(e))