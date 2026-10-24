import frappe
from frappe.utils import today, add_days

def seed_all():
    print("Seeding realistic demo data for Pest Control Manpower Allocation...")
    company = frappe.get_all("Company")[0].name

    # 1. Customers
    customers = [
        {"name": "Lulu International Mall", "group": "Commercial"},
        {"name": "Grand Hyatt Kochi", "group": "Commercial"},
        {"name": "Paragon Restaurant", "group": "Commercial"},
        {"name": "Wipro Infopark Campus", "group": "Commercial"}
    ]
    for c in customers:
        if not frappe.db.exists("Customer", c["name"]):
            cust = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": c["name"],
                "customer_type": "Company",
                "customer_group": "Commercial",
                "territory": "All Territories"
            })
            cust.insert(ignore_permissions=True)
            print(f"Created Customer: {c['name']}")

    # 2. Field Technicians (Employees)
    technicians = [
        {"first_name": "Rahul", "last_name": "Menon", "cell_number": "+91 98950 11001", "technician_certification": "Licensed Pest Technician", "pesticide_license_no": "KL-PEST-2024-881", "license_expiry_date": add_days(today(), 365)},
        {"first_name": "Akhil", "last_name": "Raj", "cell_number": "+91 98950 22002", "technician_certification": "Fumigation & Termite Specialist", "pesticide_license_no": "KL-PEST-2023-412", "license_expiry_date": add_days(today(), 400)},
        {"first_name": "Vineeth", "last_name": "Kumar", "cell_number": "+91 98950 33003", "technician_certification": "Rodent & Vector Control Specialist", "pesticide_license_no": "KL-PEST-2025-109", "license_expiry_date": add_days(today(), 500)},
        {"first_name": "Shaiju", "last_name": "Mathew", "cell_number": "+91 98950 44004", "technician_certification": "Trainee / Assistant Technician", "pesticide_license_no": "KL-PEST-2026-950", "license_expiry_date": add_days(today(), 600)},
        {"first_name": "Muhammed", "last_name": "Asif", "cell_number": "+91 98950 55005", "technician_certification": "Licensed Pest Technician", "pesticide_license_no": "KL-PEST-2024-773", "license_expiry_date": add_days(today(), 250)}
    ]

    created_employees = {}
    for t in technicians:
        full_name = f"{t['first_name']} {t['last_name']}"
        emp_name = frappe.db.get_value("Employee", {"first_name": t["first_name"], "last_name": t["last_name"]}, "name")
        if not emp_name:
            emp = frappe.get_doc({
                "doctype": "Employee",
                "first_name": t["first_name"],
                "last_name": t["last_name"],
                "gender": "Male",
                "date_of_joining": "2024-01-01",
                "date_of_birth": "1996-05-15",
                "company": company,
                "status": "Active",
                "cell_number": t["cell_number"],
                "is_pest_technician": 1,
                "technician_certification": t["technician_certification"],
                "pesticide_license_no": t["pesticide_license_no"],
                "license_expiry_date": t["license_expiry_date"]
            })
            emp.insert(ignore_permissions=True)
            emp_name = emp.name
            print(f"Created Technician Employee: {full_name} ({emp_name})")
        created_employees[full_name] = emp_name

    frappe.db.commit()

    # 3. Create Approved Leave for Muhammed Asif
    asif_id = created_employees.get("Muhammed Asif")
    if asif_id:
        existing_leave = frappe.db.get_value("Leave Application", {"employee": asif_id, "docstatus": 1})
        if not existing_leave:
            lt_list = frappe.get_all("Leave Type", limit=1)
            lt = lt_list[0].name if lt_list else "Casual Leave"

            leave = frappe.get_doc({
                "doctype": "Leave Application",
                "employee": asif_id,
                "leave_type": lt,
                "from_date": today(),
                "to_date": add_days(today(), 2),
                "status": "Approved",
                "description": "Medical recuperation following viral infection",
                "company": company
            })
            leave.insert(ignore_permissions=True)
            leave.submit()
            print(f"Created Approved Leave for Muhammed Asif from {today()} to {add_days(today(), 2)}")

    # 4. Work Order 1 & Allocation for Rahul Menon
    lulu_site = "Lulu International Mall-Food Court Level 3"
    wo1_name = frappe.db.get_value("Pest Work Order", {"customer": "Lulu International Mall"}, "name")
    if not wo1_name:
        wo1 = frappe.get_doc({
            "doctype": "Pest Work Order",
            "customer": "Lulu International Mall",
            "site": lulu_site,
            "service_type": "Commercial Cockroach & Pest Gel Treatment",
            "scheduled_date": today(),
            "time_slot": "Morning (08:00 - 12:00)",
            "priority": "High",
            "status": "Scheduled",
            "service_notes": "Monthly intensive gel baiting across 14 food stalls and central waste disposal area."
        })
        wo1.insert(ignore_permissions=True)
        wo1_name = wo1.name
        print(f"Created Pest Work Order 1: {wo1_name}")

    rahul_id = created_employees.get("Rahul Menon")
    if rahul_id and wo1_name:
        if not frappe.db.exists("Manpower Allocation", {"work_order": wo1_name, "employee": rahul_id}):
            alloc1 = frappe.get_doc({
                "doctype": "Manpower Allocation",
                "work_order": wo1_name,
                "employee": rahul_id,
                "role": "Lead Technician",
                "status": "Assigned"
            })
            alloc1.insert(ignore_permissions=True)
            alloc1.submit()
            print(f"Created Manpower Allocation for Rahul Menon -> {wo1_name}")

    frappe.db.commit()
    print("Seeding complete and committed!")