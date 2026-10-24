// Copyright (c) 2026, Gopika and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pest Control Contract", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1) {
            frm.add_custom_button(__("Generate Scheduled Work Orders"), () => {
                frappe.confirm(
                    __("Are you sure you want to auto-generate scheduled Work Orders for this contract?"),
                    () => {
                        frappe.call({
                            method: "generate_work_orders",
                            doc: frm.doc,
                            freeze: true,
                            freeze_message: __("Generating scheduled work orders..."),
                            callback: (r) => {
                                if (r.message) {
                                    frappe.msgprint({
                                        title: __("Work Orders Generated"),
                                        indicator: "green",
                                        message: __("Successfully created {0} scheduled Pest Work Orders!").format(r.message.count)
                                    });
                                }
                            }
                        });
                    }
                );
            }, __("Actions")).addClass("btn-primary");
        }
    }
});