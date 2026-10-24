import frappe
import json

def setup_workspace_content():
    print("Configuring BlockEditor content for Pest Control Workspace...")
    
    ws_name = "Pest Control & FM" if frappe.db.exists("Workspace", "Pest Control & FM") else "Pest Control"
    if not ws_name or not frappe.db.exists("Workspace", ws_name):
        print("Workspace not found!")
        return

    ws = frappe.get_doc("Workspace", ws_name)

    # 1. Shortcuts
    ws.set("shortcuts", [
        {"type": "DocType", "link_to": "Pest Work Order", "label": "Work Orders", "color": "Blue"},
        {"type": "DocType", "link_to": "Manpower Allocation", "label": "Manpower Allocation", "color": "Green"},
        {"type": "DocType", "link_to": "Pest Control Contract", "label": "Service Contracts", "color": "Purple"},
        {"type": "DocType", "link_to": "Pest Control Site", "label": "Client Sites", "color": "Orange"}
    ])

    # 2. Number cards
    ws.set("number_cards", [
        {"number_card_name": "Scheduled Jobs"},
        {"number_card_name": "Completed Jobs"},
        {"number_card_name": "Active AMC Contracts"},
        {"number_card_name": "Certified Technicians"}
    ])

    # 3. Links / Cards
    ws.set("links", [
        {"label": "Operations", "type": "Card Break"},
        {"type": "Link", "link_type": "DocType", "link_to": "Pest Work Order", "label": "Pest Work Order", "dependencies": ""},
        {"type": "Link", "link_type": "DocType", "link_to": "Manpower Allocation", "label": "Manpower Allocation", "dependencies": ""},
        {"type": "Link", "link_type": "DocType", "link_to": "Pest Control Site", "label": "Pest Control Site", "dependencies": ""},
        {"type": "Link", "link_type": "Report", "link_to": "Daily Manpower Deployment", "label": "Daily Deployment Schedule", "is_query_report": 1},
        
        {"label": "Contracts & CRM", "type": "Card Break"},
        {"type": "Link", "link_type": "DocType", "link_to": "Pest Control Contract", "label": "Pest Control Contract", "dependencies": ""},
        {"type": "Link", "link_type": "DocType", "link_to": "Customer", "label": "Customer Accounts", "dependencies": ""},
        
        {"label": "HR & Manpower Masters", "type": "Card Break"},
        {"type": "Link", "link_type": "DocType", "link_to": "Employee", "label": "Field Technicians", "dependencies": ""},
        {"type": "Link", "link_type": "DocType", "link_to": "Leave Application", "label": "Technician Leave Records", "dependencies": ""},
        {"type": "Link", "link_type": "DocType", "link_to": "Service Type", "label": "Service Types & Rates", "dependencies": ""}
    ])

    # 4. BlockEditor content JSON (CRUCIAL FOR FRAPPE V15 RENDERING)
    content_blocks = [
        {"id": "hdr_1", "type": "header", "data": {"text": "<span class=\"h4\"><b>Live Operational Summary</b></span>", "col": 12}},
        {"id": "nc_1", "type": "number_card", "data": {"number_card_name": "Scheduled Jobs", "col": 3}},
        {"id": "nc_2", "type": "number_card", "data": {"number_card_name": "Completed Jobs", "col": 3}},
        {"id": "nc_3", "type": "number_card", "data": {"number_card_name": "Active AMC Contracts", "col": 3}},
        {"id": "nc_4", "type": "number_card", "data": {"number_card_name": "Certified Technicians", "col": 3}},
        {"id": "spc_1", "type": "spacer", "data": {"col": 12}},
        {"id": "hdr_2", "type": "header", "data": {"text": "<span class=\"h4\"><b>Operations &amp; Dispatch Shortcuts</b></span>", "col": 12}},
        {"id": "sc_1", "type": "shortcut", "data": {"shortcut_name": "Work Orders", "col": 3}},
        {"id": "sc_2", "type": "shortcut", "data": {"shortcut_name": "Manpower Allocation", "col": 3}},
        {"id": "sc_3", "type": "shortcut", "data": {"shortcut_name": "Service Contracts", "col": 3}},
        {"id": "sc_4", "type": "shortcut", "data": {"shortcut_name": "Client Sites", "col": 3}},
        {"id": "spc_2", "type": "spacer", "data": {"col": 12}},
        {"id": "hdr_3", "type": "header", "data": {"text": "<span class=\"h4\"><b>Modules &amp; Masters</b></span>", "col": 12}},
        {"id": "cd_1", "type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"id": "cd_2", "type": "card", "data": {"card_name": "Contracts & CRM", "col": 4}},
        {"id": "cd_3", "type": "card", "data": {"card_name": "HR & Manpower Masters", "col": 4}}
    ]

    ws.content = json.dumps(content_blocks)
    ws.public = 1
    ws.is_standard = 1
    ws.save(ignore_permissions=True)
    frappe.db.commit()
    print("Pest Control Workspace successfully updated with rich BlockEditor layout!")