frappe.views.calendar["Pest Work Order"] = {
    field_map: {
        start: "scheduled_date",
        end: "scheduled_date",
        id: "name",
        title: "customer",
        allDay: "allDay"
    },
    style_map: {
        "Draft": "secondary",
        "Scheduled": "info",
        "In Progress": "warning",
        "Completed": "success",
        "Cancelled": "danger"
    },
    get_events_method: "frappe.desk.calendar.get_events"
};