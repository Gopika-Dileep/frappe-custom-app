frappe.views.calendar["Manpower Allocation"] = {
    field_map: {
        start: "allocation_date",
        end: "allocation_date",
        id: "name",
        title: "employee_name",
        allDay: "allDay"
    },
    style_map: {
        "Assigned": "info",
        "Dispatched": "warning",
        "On Site": "primary",
        "Completed": "success",
        "Absent / Reassigned": "danger"
    },
    get_events_method: "frappe.desk.calendar.get_events"
};