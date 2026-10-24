import frappe

def setup_cards_and_workspace():
    print("Linking Number Cards to Workspace Dashboard...")
    cards = [
        "Scheduled Jobs",
        "Completed Jobs",
        "Active AMC Contracts",
        "Certified Technicians"
    ]

    ws_name = "Pest Control & FM" if frappe.db.exists("Workspace", "Pest Control & FM") else "Pest Control"
    if ws_name and frappe.db.exists("Workspace", ws_name):
        ws = frappe.get_doc("Workspace", ws_name)
        ws.set("number_cards", [])
        for c in cards:
            if frappe.db.exists("Number Card", c):
                ws.append("number_cards", {"number_card_name": c})
        ws.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"Updated Workspace '{ws_name}' with Number Cards!")