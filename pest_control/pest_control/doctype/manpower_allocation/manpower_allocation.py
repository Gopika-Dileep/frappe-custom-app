# Copyright (c) 2026, Gopika and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class ManpowerAllocation(Document):
    def validate(self):
        self.fetch_work_order_details()
        self.validate_employee_status()
        self.validate_leave_status()
        self.validate_company_holiday()
        self.validate_shift_assignment()
        self.validate_double_booking()
        self.validate_technician_license()

    def fetch_work_order_details(self):
        if self.work_order:
            wo = frappe.get_doc("Pest Work Order", self.work_order)
            self.customer = wo.customer
            self.site = wo.site
            self.service_type = wo.service_type
            self.allocation_date = wo.scheduled_date
            self.time_slot = wo.time_slot
            if not self.employee_name and self.employee:
                self.employee_name = frappe.db.get_value("Employee", self.employee, "employee_name")

    def validate_employee_status(self):
        """Cross-checks Frappe HR Employee master to verify technician is active."""
        emp_status = frappe.db.get_value("Employee", self.employee, "status")
        if emp_status and emp_status != "Active":
            frappe.throw(_("Technician {0} ({1}) is inactive or relieved (Status: {2}). Cannot assign to field work.").format(
                self.employee_name or self.employee, self.employee, emp_status
            ))

    def validate_leave_status(self):
        """Cross-checks Frappe HR Leave Application to guarantee worker is not on approved personal leave."""
        leaves = frappe.db.sql("""
            SELECT name, leave_type, from_date, to_date
            FROM `tabLeave Application`
            WHERE employee = %s
              AND docstatus = 1
              AND status = 'Approved'
              AND %s BETWEEN from_date AND to_date
        """, (self.employee, self.allocation_date), as_dict=True)

        if leaves:
            leave = leaves[0]
            frappe.throw(_(
                "Allocation Error: Technician {0} ({1}) is on approved {2} Leave from {3} to {4} (Ref: {5}). Please allocate a different technician."
            ).format(
                self.employee_name or self.employee,
                self.employee,
                leave.leave_type,
                leave.from_date,
                leave.to_date,
                leave.name
            ))

    def validate_company_holiday(self):
        """Cross-checks Frappe HR / ERPNext Holiday List to check for declared company holidays / weekly offs."""
        if not self.employee or not self.allocation_date:
            return

        if self.flags.ignore_holiday or self.get("allow_holiday_work"):
            return

        # Fetch employee's assigned Holiday List or fallback to company default
        holiday_list = frappe.db.get_value("Employee", self.employee, "holiday_list")
        if not holiday_list:
            company = frappe.db.get_value("Employee", self.employee, "company") or frappe.defaults.get_user_default("company")
            if company:
                holiday_list = frappe.db.get_value("Company", company, "default_holiday_list")

        if not holiday_list:
            hl_match = frappe.db.sql("""
                SELECT name FROM `tabHoliday List`
                WHERE %s BETWEEN from_date AND to_date
                ORDER BY from_date DESC LIMIT 1
            """, (self.allocation_date,), as_dict=True)
            if hl_match:
                holiday_list = hl_match[0].name

        if holiday_list:
            holidays = frappe.db.sql("""
                SELECT description, weekly_off
                FROM `tabHoliday`
                WHERE parent = %s AND holiday_date = %s
            """, (holiday_list, self.allocation_date), as_dict=True)

            if holidays:
                h = holidays[0]
                holiday_type = "Weekly Off" if h.weekly_off else "Company Holiday"
                frappe.throw(_(
                    "Allocation Error: Date {0} is a declared {1} ({2}) in Holiday List '{3}' for Technician {4}. Enable 'Permit Allocation on Company Holiday' if emergency overtime is approved."
                ).format(
                    self.allocation_date,
                    holiday_type,
                    h.description or holiday_type,
                    holiday_list,
                    self.employee_name or self.employee
                ))

    def validate_shift_assignment(self):
        """Cross-checks Frappe HR Shift Assignment to verify active working shift."""
        if not self.employee or not self.allocation_date:
            return

        shift = frappe.db.sql("""
            SELECT shift_type
            FROM `tabShift Assignment`
            WHERE employee = %s
              AND %s >= start_date
              AND (end_date IS NULL OR %s <= end_date)
              AND docstatus = 1
              AND status = 'Active'
            LIMIT 1
        """, (self.employee, self.allocation_date, self.allocation_date), as_dict=True)

        if shift and not self.notes:
            self.notes = f"Allocated under active shift: {shift[0].shift_type}"

    def validate_double_booking(self):
        """Prevents scheduling the same technician on overlapping jobs on the same date and shift."""
        query = """
            SELECT name, work_order, time_slot, status
            FROM `tabManpower Allocation`
            WHERE employee = %s
              AND allocation_date = %s
              AND time_slot = %s
              AND docstatus < 2
              AND name != %s
        """
        conflicts = frappe.db.sql(query, (
            self.employee,
            self.allocation_date,
            self.time_slot,
            self.name or ""
        ), as_dict=True)

        if conflicts:
            c = conflicts[0]
            frappe.throw(_(
                "Double-Booking Conflict! Technician {0} ({1}) is ALREADY allocated to Work Order {2} during the '{3}' shift on {4} (Allocation Ref: {5})."
            ).format(
                self.employee_name or self.employee,
                self.employee,
                c.work_order,
                c.time_slot,
                self.allocation_date,
                c.name
            ))

    def validate_technician_license(self):
        """Ensures technician pesticide license is valid."""
        expiry = frappe.db.get_value("Employee", self.employee, "license_expiry_date")
        if expiry and str(expiry) < str(self.allocation_date):
            frappe.throw(_(
                "Technician {0}'s pesticide handling license expired on {1}! License renewal required before deployment."
            ).format(self.employee_name or self.employee, expiry))

    def record_attendance_on_completion(self):
        """Synchronizes with Frappe HR Attendance ledger when technician performs field service."""
        if not self.employee or not self.allocation_date:
            return

        if self.status not in ["Completed", "On Site"]:
            return

        existing = frappe.db.get_value(
            "Attendance",
            {"employee": self.employee, "attendance_date": self.allocation_date, "docstatus": ["<", 2]},
            ["name", "status"],
            as_dict=True
        )

        if not existing:
            att = frappe.get_doc({
                "doctype": "Attendance",
                "employee": self.employee,
                "attendance_date": self.allocation_date,
                "status": "Present",
                "remarks": f"Auto-marked via Pest Manpower Allocation {self.name} for Work Order {self.work_order}"
            })
            att.insert(ignore_permissions=True)
            att.submit()
            frappe.msgprint(_("Technician {0} attendance auto-recorded as 'Present' for {1}.").format(
                self.employee_name or self.employee, self.allocation_date
            ))
        elif existing.status != "Present":
            frappe.db.set_value("Attendance", existing.name, "status", "Present")

    def on_submit(self):
        # Synchronize back to Pest Work Order child table
        if self.work_order:
            wo = frappe.get_doc("Pest Work Order", self.work_order)
            already_listed = False
            for tech in wo.allocated_technicians:
                if tech.employee == self.employee:
                    tech.manpower_allocation = self.name
                    tech.role = self.role
                    already_listed = True
                    break
            
            if not already_listed:
                wo.append("allocated_technicians", {
                    "employee": self.employee,
                    "employee_name": self.employee_name,
                    "role": self.role,
                    "contact_number": frappe.db.get_value("Employee", self.employee, "cell_number"),
                    "manpower_allocation": self.name
                })
            
            if wo.status == "Draft":
                wo.status = "Scheduled"
            
            wo.save(ignore_permissions=True)
            frappe.msgprint(_("Technician {0} linked to Work Order {1}").format(self.employee_name, self.work_order))

        self.record_attendance_on_completion()

    def on_update(self):
        if self.status == "Completed":
            self.record_attendance_on_completion()

    def on_cancel(self):
        if self.work_order:
            wo = frappe.get_doc("Pest Work Order", self.work_order)
            wo.allocated_technicians = [t for t in wo.allocated_technicians if t.employee != self.employee]
            wo.save(ignore_permissions=True)
