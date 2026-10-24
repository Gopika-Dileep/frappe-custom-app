import frappe
from frappe.utils import today, add_days

def add_completed_jobs():
    print("Adding additional realistic completed pest jobs with chemical logs...")
    
    # 1. Completed Job at Paragon Restaurant
    paragon_site = "Paragon Restaurant-Central Dine-in & Storage"
    akhil_id = frappe.db.get_value("Employee", {"employee_name": "Akhil Raj"}, "name")
    shaiju_id = frappe.db.get_value("Employee", {"employee_name": "Shaiju Mathew"}, "name")
    
    if not frappe.db.exists("Pest Work Order", {"customer": "Paragon Restaurant"}):
        wo = frappe.get_doc({
            "doctype": "Pest Work Order",
            "customer": "Paragon Restaurant",
            "site": paragon_site,
            "service_type": "Commercial Cockroach & Pest Gel Treatment",
            "scheduled_date": add_days(today(), -1),
            "time_slot": "Morning (08:00 - 12:00)",
            "priority": "High",
            "status": "Completed",
            "completion_date": add_days(today(), -1),
            "client_feedback": "Excellent",
            "technician_remarks": "Completed intensive food-grade gel baiting across 8 kitchen prep stations and drainage gullies. Trap catch low, pest activity controlled.",
            "supervisor_notes": "Passed hygiene quality inspection.",
            "chemicals_used": [
                {
                    "chemical_name": "Advion Cockroach Gel Bait",
                    "active_ingredient": "Indoxacarb 0.6%",
                    "quantity_used": 60.0,
                    "unit_of_measure": "grams",
                    "batch_no": "ADV-2026-901",
                    "targeted_pest": "German Cockroach"
                },
                {
                    "chemical_name": "Temprid SC Insecticide",
                    "active_ingredient": "Imidacloprid 21% + Beta-Cyfluthrin 10.5%",
                    "quantity_used": 150.0,
                    "unit_of_measure": "ml",
                    "batch_no": "TMP-2026-442",
                    "targeted_pest": "Ants & Perimeter Crawling Insects"
                }
            ],
            "allocated_technicians": [
                {
                    "employee": akhil_id,
                    "role": "Lead Technician"
                },
                {
                    "employee": shaiju_id,
                    "role": "Assistant Technician"
                }
            ]
        })
        wo.insert(ignore_permissions=True)
        print(f"Created Completed Work Order at Paragon: {wo.name}")
        
        # Create corresponding historical allocations
        if akhil_id:
            alloc_a = frappe.get_doc({
                "doctype": "Manpower Allocation",
                "work_order": wo.name,
                "employee": akhil_id,
                "role": "Lead Technician",
                "status": "Completed"
            })
            alloc_a.insert(ignore_permissions=True)
            alloc_a.submit()
            
        if shaiju_id:
            alloc_s = frappe.get_doc({
                "doctype": "Manpower Allocation",
                "work_order": wo.name,
                "employee": shaiju_id,
                "role": "Assistant Technician",
                "status": "Completed"
            })
            alloc_s.insert(ignore_permissions=True)
            alloc_s.submit()

    # 2. Completed Job at Wipro Campus (Termite Barrier Treatment)
    wipro_site = "Wipro Infopark Campus-Tower B Server & Workstation Wings"
    vineeth_id = frappe.db.get_value("Employee", {"employee_name": "Vineeth Kumar"}, "name")
    
    if not frappe.db.exists("Pest Work Order", {"customer": "Wipro Infopark Campus"}):
        wo2 = frappe.get_doc({
            "doctype": "Pest Work Order",
            "customer": "Wipro Infopark Campus",
            "site": wipro_site,
            "service_type": "Subterranean Termite Barrier Treatment",
            "scheduled_date": add_days(today(), -2),
            "time_slot": "Afternoon (13:00 - 17:00)",
            "priority": "Standard",
            "status": "Completed",
            "completion_date": add_days(today(), -2),
            "client_feedback": "Good",
            "technician_remarks": "Subterranean barrier trenching along server room external wall completed. 40 injection points treated with Premise 200 SC.",
            "supervisor_notes": "Safe drill protocols observed near underground cabling.",
            "chemicals_used": [
                {
                    "chemical_name": "Premise 200 SC Termiticide",
                    "active_ingredient": "Imidacloprid 200 g/L",
                    "quantity_used": 5.0,
                    "unit_of_measure": "Litre",
                    "batch_no": "PRM-2026-118",
                    "targeted_pest": "Subterranean Termites"
                }
            ],
            "allocated_technicians": [
                {
                    "employee": vineeth_id,
                    "role": "Lead Technician"
                }
            ]
        })
        wo2.insert(ignore_permissions=True)
        print(f"Created Completed Work Order at Wipro: {wo2.name}")
        
        if vineeth_id:
            alloc_v = frappe.get_doc({
                "doctype": "Manpower Allocation",
                "work_order": wo2.name,
                "employee": vineeth_id,
                "role": "Lead Technician",
                "status": "Completed"
            })
            alloc_v.insert(ignore_permissions=True)
            alloc_v.submit()

    frappe.db.commit()
    print("All additional realistic completed records committed successfully!")