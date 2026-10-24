import frappe

def create_print_format():
    print("Setting up Pest Service Certificate Print Format...")
    
    html_content = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; padding: 20px;">
    <!-- Header -->
    <div style="border-bottom: 2px solid #0284c7; padding-bottom: 15px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 0; color: #0f172a; font-size: 24px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Pest Control Service Certificate</h2>
                <div style="color: #64748b; font-size: 13px; margin-top: 4px;">Facility Management & Soft Services Division | Chemical Compliance Record</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 16px; font-weight: 700; color: #0284c7;">{{ doc.name }}</div>
                <div style="font-size: 12px; color: #64748b;">Date: {{ frappe.utils.format_date(doc.scheduled_date) }}</div>
                <div style="margin-top: 4px;"><span style="display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; background: #e0f2fe; color: #0369a1;">{{ doc.status }}</span></div>
            </div>
        </div>
    </div>

    <!-- Client & Facility Information Grid -->
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px;">
        <tr style="background: #f8fafc;">
            <td style="padding: 10px; width: 25%; font-weight: 600; color: #475569; border: 1px solid #e2e8f0;">Customer / Client:</td>
            <td style="padding: 10px; width: 25%; border: 1px solid #e2e8f0; font-weight: 600;">{{ doc.customer_name or doc.customer }}</td>
            <td style="padding: 10px; width: 25%; font-weight: 600; color: #475569; border: 1px solid #e2e8f0;">Service Facility Site:</td>
            <td style="padding: 10px; width: 25%; border: 1px solid #e2e8f0;">{{ doc.site }}</td>
        </tr>
        <tr>
            <td style="padding: 10px; font-weight: 600; color: #475569; border: 1px solid #e2e8f0;">Service Type:</td>
            <td style="padding: 10px; border: 1px solid #e2e8f0; color: #0284c7; font-weight: 600;">{{ doc.service_type }}</td>
            <td style="padding: 10px; font-weight: 600; color: #475569; border: 1px solid #e2e8f0;">Shift / Time Slot:</td>
            <td style="padding: 10px; border: 1px solid #e2e8f0;">{{ doc.time_slot }}</td>
        </tr>
        <tr style="background: #f8fafc;">
            <td style="padding: 10px; font-weight: 600; color: #475569; border: 1px solid #e2e8f0;">Contract Reference:</td>
            <td style="padding: 10px; border: 1px solid #e2e8f0;">{{ doc.contract or "Standard Work Order" }}</td>
            <td style="padding: 10px; font-weight: 600; color: #475569; border: 1px solid #e2e8f0;">Priority Level:</td>
            <td style="padding: 10px; border: 1px solid #e2e8f0;">{{ doc.priority }}</td>
        </tr>
    </table>

    <!-- Deployed Manpower Crew -->
    <div style="margin-bottom: 20px;">
        <h4 style="margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase; color: #334155; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px;">1. Deployed Manpower & Field Technicians</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
            <thead>
                <tr style="background: #f1f5f9; text-align: left;">
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">#</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Technician Name</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Role</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Contact Number</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Allocation Ref</th>
                </tr>
            </thead>
            <tbody>
                {% for tech in doc.allocated_technicians %}
                <tr>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ loop.index }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: 600;">{{ tech.employee_name }} ({{ tech.employee }})</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ tech.role }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ tech.contact_number or "-" }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0; color: #64748b;">{{ tech.manpower_allocation or "-" }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5" style="padding: 10px; text-align: center; color: #94a3b8; border: 1px solid #e2e8f0;">No technicians allocated yet.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Chemicals & Consumables Applied Table -->
    <div style="margin-bottom: 25px;">
        <h4 style="margin: 0 0 8px 0; font-size: 14px; text-transform: uppercase; color: #334155; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px;">2. Chemical Application & Consumption Log (Compliance)</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
            <thead>
                <tr style="background: #f1f5f9; text-align: left;">
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">#</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Chemical / Pesticide</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Active Ingredient</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Quantity Applied</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Batch No</th>
                    <th style="padding: 8px; border: 1px solid #cbd5e1;">Target Pest</th>
                </tr>
            </thead>
            <tbody>
                {% for chem in doc.chemicals_used %}
                <tr>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ loop.index }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0; font-weight: 600;">{{ chem.chemical_name }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ chem.active_ingredient or "-" }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ chem.quantity_used }} {{ chem.unit_of_measure }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ chem.batch_no or "-" }}</td>
                    <td style="padding: 8px; border: 1px solid #e2e8f0;">{{ chem.targeted_pest or "-" }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="6" style="padding: 10px; text-align: center; color: #94a3b8; border: 1px solid #e2e8f0;">Standard gel bait and perimeter inspection performed.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Observations & Sign-off Block -->
    <div style="border: 1px solid #e2e8f0; padding: 12px; border-radius: 4px; margin-bottom: 30px; background: #fafafa; font-size: 12px;">
        <strong>Technician Observations & Safety Notes:</strong>
        <p style="margin: 6px 0 0 0; color: #475569;">{{ doc.technician_remarks or "All food preparation counters, drainage traps, and perimeter harborage points thoroughly treated with food-grade gel. Zero safety incidents reported." }}</p>
    </div>

    <!-- Sign-off signatures -->
    <div style="display: flex; justify-content: space-between; margin-top: 50px;">
        <div style="width: 45%; border-top: 1px solid #94a3b8; padding-top: 8px; text-align: center; font-size: 12px;">
            <div style="font-weight: 600;">Lead Technician Signature</div>
            <div style="color: #64748b; font-size: 11px;">Certified Chemical Applicator</div>
        </div>
        <div style="width: 45%; border-top: 1px solid #94a3b8; padding-top: 8px; text-align: center; font-size: 12px;">
            <div style="font-weight: 600;">Client / Facility Manager Sign-off</div>
            <div style="color: #64748b; font-size: 11px;">Client Satisfaction: <strong>{{ doc.client_feedback or "Good" }}</strong></div>
        </div>
    </div>
</div>
"""

    if not frappe.db.exists("Print Format", "Pest Service Certificate"):
        pf = frappe.get_doc({
            "doctype": "Print Format",
            "name": "Pest Service Certificate",
            "doc_type": "Pest Work Order",
            "module": "Pest Control",
            "standard": "Yes",
            "custom_format": 1,
            "print_format_type": "Jinja",
            "html": html_content
        })
        pf.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created Pest Service Certificate Print Format!")
    else:
        pf = frappe.get_doc("Print Format", "Pest Service Certificate")
        pf.html = html_content
        pf.save(ignore_permissions=True)
        frappe.db.commit()
        print("Updated Pest Service Certificate Print Format!")
