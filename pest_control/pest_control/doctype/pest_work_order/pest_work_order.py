# Copyright (c) 2026, Gopika and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PestWorkOrder(Document):
    def validate(self):
        # Auto-fetch area if missing
        if self.site and not self.area_sqft:
            self.area_sqft = frappe.db.get_value("Pest Control Site", self.site, "area_sqft") or 0.0
            
        # Auto-fetch rate if missing
        if self.service_type and not self.service_rate:
            self.service_rate = frappe.db.get_value("Service Type", self.service_type, "standard_rate") or 0.0
            
        # Default billing_amount to service_rate if zero or empty
        if not self.billing_amount and self.service_rate:
            self.billing_amount = self.service_rate
