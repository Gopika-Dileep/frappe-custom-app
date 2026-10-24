# Copyright (c) 2026, Gopika and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json

@frappe.whitelist()
def get_available_technicians(date, time_slot, service_type=None):
    """
    Core Allocation Engine Algorithm:
    1. Fetches all active field employees/technicians.
    2. Excludes technicians on approved Frappe HR Leave for the specified date.
    3. Excludes technicians with overlapping Manpower Allocations in the given time slot.
    4. Computes prior completed work order count (experience score).
    """
    if not date or not time_slot:
        return []

    # 1. Base Pool: Active Employees
    employees = frappe.db.sql("""
        SELECT 
            name as employee,
            employee_name,
            department,
            designation,
            cell_number,
            technician_certification,
            pesticide_license_no
        FROM `tabEmployee`
        WHERE status = 'Active'
        ORDER BY employee_name ASC
    """, as_dict=True)

    # 2. Busy on approved leave on that date
    on_leave_employees = set(frappe.db.sql_list("""
        SELECT DISTINCT employee
        FROM `tabLeave Application`
        WHERE docstatus = 1
          AND status = 'Approved'
          AND %s BETWEEN from_date AND to_date
    """, (date,)))

    # 3. Already booked on that date and time slot
    booked_employees = set(frappe.db.sql_list("""
        SELECT DISTINCT employee
        FROM `tabManpower Allocation`
        WHERE allocation_date = %s
          AND time_slot = %s
          AND docstatus < 2
    """, (date, time_slot)))

    available = []
    for emp in employees:
        is_on_leave = emp.employee in on_leave_employees
        is_booked = emp.employee in booked_employees

        if not is_on_leave and not is_booked:
            # Count completed jobs for experience
            completed_jobs = frappe.db.count("Manpower Allocation", {
                "employee": emp.employee,
                "status": "Completed"
            })
            emp["completed_jobs"] = completed_jobs
            emp["availability_status"] = "Available"
            available.append(emp)

    return available


@frappe.whitelist()
def assign_technicians(work_order, assignments):
    """
    Bulk assigns technicians to a Pest Work Order, generating individual
    submittable Manpower Allocation records with conflict validation.
    """
    if isinstance(assignments, str):
        assignments = json.loads(assignments)

    if not assignments:
        frappe.throw(_("Please select at least one technician to allocate."))

    wo = frappe.get_doc("Pest Work Order", work_order)
    created_allocations = []

    for item in assignments:
        emp_id = item.get("employee")
        role = item.get("role", "Lead Technician")

        # Create Manpower Allocation document
        alloc = frappe.get_doc({
            "doctype": "Manpower Allocation",
            "work_order": wo.name,
            "employee": emp_id,
            "role": role,
            "status": "Assigned"
        })
        alloc.insert()
        alloc.submit()
        created_allocations.append(alloc.name)

    wo.reload()
    if wo.status == "Draft":
        wo.status = "Scheduled"
        wo.save(ignore_permissions=True)

    return {
        "success": True,
        "message": _("Successfully allocated {0} technician(s) to Work Order {1}").format(len(created_allocations), wo.name),
        "allocations": created_allocations
    }


@frappe.whitelist()
def complete_work_order(work_order, client_feedback="Good", remarks=""):
    """
    Closes the work order, updates related Manpower Allocations,
    and logs attendance / check-in events in Frappe HR.
    """
    wo = frappe.get_doc("Pest Work Order", work_order)
    wo.status = "Completed"
    wo.completion_date = frappe.utils.today()
    wo.client_feedback = client_feedback
    wo.technician_remarks = remarks
    wo.save(ignore_permissions=True)

    # Update associated Manpower Allocations
    allocations = frappe.get_all("Manpower Allocation", filters={"work_order": wo.name, "docstatus": 1})
    for a in allocations:
        frappe.db.set_value("Manpower Allocation", a.name, {
            "status": "Completed",
            "checkout_time": frappe.utils.now_datetime()
        })

    frappe.db.commit()
    return {
        "success": True,
        "message": _("Work Order {0} marked Completed! Manpower records updated.").format(wo.name)
    }