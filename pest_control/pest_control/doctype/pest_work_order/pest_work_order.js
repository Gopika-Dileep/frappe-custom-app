// Copyright (c) 2026, Gopika and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pest Work Order", {
    site(frm) {
        if (frm.doc.site) {
            frappe.db.get_value("Pest Control Site", frm.doc.site, "area_sqft", (r) => {
                if (r && r.area_sqft) {
                    frm.set_value("area_sqft", r.area_sqft);
                }
            });
        }
    },

    service_type(frm) {
        if (frm.doc.service_type) {
            frappe.db.get_value("Service Type", frm.doc.service_type, "standard_rate", (r) => {
                if (r && r.standard_rate) {
                    frm.set_value("service_rate", r.standard_rate);
                    if (!frm.doc.billing_amount || frm.doc.billing_amount === 0) {
                        frm.set_value("billing_amount", r.standard_rate);
                    }
                }
            });
        }
    },

    service_rate(frm) {
        if (!frm.doc.billing_amount && frm.doc.service_rate) {
            frm.set_value("billing_amount", frm.doc.service_rate);
        }
    },

    refresh(frm) {
        // Status indicator badges
        frm.page.set_indicator(
            frm.doc.status === "Completed" ? "green" :
            frm.doc.status === "In Progress" ? "orange" :
            frm.doc.status === "Scheduled" ? "blue" : "gray",
            frm.doc.status
        );

        if (!frm.is_new()) {
            // 1. Smart Manpower Allocation Button
            if (frm.doc.status !== "Completed" && frm.doc.status !== "Cancelled") {
                frm.add_custom_button(__("Smart Allocate Manpower"), () => {
                    open_allocation_dialog(frm);
                }, __("Actions")).addClass("btn-primary");
            }

            // 2. Start Work Order
            if (frm.doc.status === "Scheduled") {
                frm.add_custom_button(__("Mark In Progress"), () => {
                    frm.set_value("status", "In Progress");
                    frm.save();
                }, __("Actions"));
            }

            // 3. Complete Work Order
            if (frm.doc.status === "In Progress" || frm.doc.status === "Scheduled") {
                frm.add_custom_button(__("Complete Service"), () => {
                    open_completion_dialog(frm);
                }, __("Actions")).addClass("btn-success");
            }
        }
    }
});

function open_allocation_dialog(frm) {
    frappe.call({
        method: "pest_control.api.get_available_technicians",
        args: {
            date: frm.doc.scheduled_date,
            time_slot: frm.doc.time_slot,
            service_type: frm.doc.service_type
        },
        freeze: true,
        freeze_message: __("Analyzing technician schedules and availability..."),
        callback: (r) => {
            const techs = r.message || [];
            if (techs.length === 0) {
                frappe.msgprint({
                    title: __("No Technicians Available"),
                    indicator: "red",
                    message: __("All technicians are either booked on other jobs or on approved leave for {0} ({1}).").format(frm.doc.scheduled_date, frm.doc.time_slot)
                });
                return;
            }

            let dialog_fields = [
                {
                    fieldname: "info_html",
                    fieldtype: "HTML",
                    options: `
                        <div class="alert alert-info py-2 mb-3">
                            <strong>Work Order:</strong> ${frm.doc.name} | <strong>Site:</strong> ${frm.doc.site || frm.doc.customer} | <strong>Shift:</strong> ${frm.doc.time_slot}
                        </div>
                        <p class="text-muted small">Select the available technicians to deploy for this service:</p>
                    `
                }
            ];

            techs.forEach((t, idx) => {
                const safe_id = t.employee.replace(/[^a-zA-Z0-9_]/g, '_');
                dialog_fields.push({
                    fieldname: `select_${safe_id}`,
                    label: `${t.employee_name} [${t.designation || "Field Technician"}] - ${t.technician_certification || "Certified"}`,
                    fieldtype: "Check"
                });
                dialog_fields.push({
                    fieldname: `role_${safe_id}`,
                    label: `Role for ${t.employee_name}`,
                    fieldtype: "Select",
                    options: "Lead Technician\nAssistant Technician\nChemical Sprayer\nQuality Inspector",
                    default: idx === 0 ? "Lead Technician" : "Assistant Technician",
                    depends_on: `eval:doc.select_${safe_id} == 1`
                });
            });

            const d = new frappe.ui.Dialog({
                title: __("Smart Manpower Dispatcher"),
                fields: dialog_fields,
                primary_action_label: __("Deploy Technicians"),
                primary_action: (values) => {
                    let assignments = [];
                    techs.forEach(t => {
                        const safe_id = t.employee.replace(/[^a-zA-Z0-9_]/g, '_');
                        if (values[`select_${safe_id}`]) {
                            assignments.push({
                                employee: t.employee,
                                role: values[`role_${safe_id}`] || "Lead Technician"
                            });
                        }
                    });

                    if (assignments.length === 0) {
                        frappe.msgprint(__("Please select at least one technician."));
                        return;
                    }

                    frappe.call({
                        method: "pest_control.api.assign_technicians",
                        args: {
                            work_order: frm.doc.name,
                            assignments: assignments
                        },
                        freeze: true,
                        freeze_message: __("Validating allocations and updating records..."),
                        callback: (res) => {
                            if (res.message && res.message.success) {
                                frappe.show_alert({ message: res.message.message, indicator: "green" });
                                d.hide();
                                frm.reload_doc();
                            }
                        }
                    });
                }
            });

            d.show();
        }
    });
}

function open_completion_dialog(frm) {
    const d = new frappe.ui.Dialog({
        title: __("Complete Pest Control Service"),
        fields: [
            {
                fieldname: "client_feedback",
                label: __("Client Satisfaction"),
                fieldtype: "Select",
                options: "Excellent\nGood\nSatisfactory\nUnsatisfactory",
                default: "Good",
                reqd: 1
            },
            {
                fieldname: "remarks",
                label: __("Service Execution Remarks"),
                fieldtype: "Small Text",
                placeholder: __("Enter technician observations, chemical applications, client feedback...")
            }
        ],
        primary_action_label: __("Submit & Mark Completed"),
        primary_action: (values) => {
            frappe.call({
                method: "pest_control.api.complete_work_order",
                args: {
                    work_order: frm.doc.name,
                    client_feedback: values.client_feedback,
                    remarks: values.remarks || ""
                },
                freeze: true,
                callback: (res) => {
                    if (res.message && res.message.success) {
                        frappe.show_alert({ message: res.message.message, indicator: "green" });
                        d.hide();
                        frm.reload_doc();
                    }
                }
            });
        }
    });

    d.show();
}
