import frappe

def run():
    print("=== LEAVE PERIODS ===")
    lps = frappe.get_all("Leave Period", fields=["*"])
    for lp in lps:
        print(lp)

    print("\n=== LEAVE TYPES IN DB ===")
    lts = frappe.get_all("Leave Type", fields=["name", "leave_type_name", "is_lwp", "max_leaves_allowed"])
    for lt in lts:
        print(lt)

    print("\n=== EXISTING LEAVE ALLOCATIONS ===")
    las = frappe.get_all("Leave Allocation", fields=["name", "employee", "leave_type", "new_leaves_allocated", "from_date", "to_date", "docstatus"])
    for la in las:
        print(la)
