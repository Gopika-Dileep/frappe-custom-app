# Copyright (c) 2026, Gopika and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_months, add_days, getdate
from frappe import _

class PestControlContract(Document):
    def validate(self):
        if self.end_date and self.start_date and getdate(self.end_date) < getdate(self.start_date):
            frappe.throw(_("End Date cannot be before Start Date"))
            
        # Calculate total contract amount from services
        total = 0
        for s in self.services:
            if s.rate_per_visit and s.visits_per_year:
                s.total_service_amount = s.rate_per_visit * s.visits_per_year
                total += s.total_service_amount
        if total > 0 and not self.contract_amount:
            self.contract_amount = total

    def on_submit(self):
        self.status = "Active"

    @frappe.whitelist()
    def generate_work_orders(self):
        """Generates periodic work orders across the contract duration."""
        if not self.services:
            frappe.throw(_("Please add at least one service to the contract before generating work orders."))

        created_orders = []
        for s in self.services:
            num_visits = s.visits_per_year or 1
            if num_visits <= 0:
                num_visits = 1
                
            months_step = 12 / num_visits if num_visits > 0 else 1
            
            for i in range(num_visits):
                visit_date = add_months(self.start_date, int(i * months_step))
                if getdate(visit_date) > getdate(self.end_date):
                    break

                wo = frappe.get_doc({
                    "doctype": "Pest Work Order",
                    "customer": self.customer,
                    "site": self.site,
                    "contract": self.name,
                    "service_type": s.service_type,
                    "scheduled_date": visit_date,
                    "time_slot": "Morning (08:00 - 12:00)",
                    "priority": "Standard",
                    "status": "Draft",
                    "service_notes": f"Contract Visit #{i+1} for {s.service_type}"
                })
                wo.insert(ignore_permissions=True)
                created_orders.append(wo.name)

        frappe.db.commit()
        return {
            "count": len(created_orders),
            "orders": created_orders
        }