# Pest Control & Facility Management ERP

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15-blue.svg)](https://frappeframework.com)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15-blueviolet.svg)](https://erpnext.com)
[![Frappe HR](https://img.shields.io/badge/Frappe%20HR-v15-orange.svg)](https://frappehr.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](license.txt)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A comprehensive, production-ready enterprise Frappe custom application tailored for **Pest Control**, **Manpower Allocation**, and **Facility Management** service providers.

Seamlessly integrated with **ERPNext** (CRM, Inventory, Billing) and **Frappe HR** (Employees, Shift Schedules, Leave Applications, Attendance Tracking), this application handles the complete end-to-end operational lifecycle: from multi-site contract management to conflict-free technician dispatch, chemical tracking, digital certificates, and automated HR attendance.

---

## Table of Contents

- [Key Features](#key-features)
- [System Architecture & Lifecycle](#system-architecture--lifecycle)
- [Core Modules & DocTypes](#core-modules--doctypes)
  - [1. Operations & Work Orders](#1-operations--work-orders)
  - [2. Smart Manpower Allocation Engine](#2-smart-manpower-allocation-engine)
  - [3. Facility & Contract Management](#3-facility--contract-management)
- [HR & ERPNext Integrations](#hr--erpnext-integrations)
- [Reports & Executive Dashboard](#reports--executive-dashboard)
- [Whitelisted REST APIs](#whitelisted-rest-apis)
- [Installation Guide](#installation-guide)
- [Development & Code Quality](#development--code-quality)
- [License & Author](#license--author)

---

## Key Features

- **Field Work Order Management:** Full tracking of service tickets (`Draft` &rarr; `Scheduled` &rarr; `In Progress` &rarr; `Completed`), shift slots, priority levels, and client ratings.
- **Automated Conflict-Free Manpower Dispatch:**
  - Double-booking prevention across shifts and dates.
  - Automatic cross-check against Frappe HR approved **Leave Applications**.
  - Cross-check against declared **Company Holiday Lists** and weekly offs (with emergency overtime approval flags).
  - Real-time verification of technician **Pesticide Handling Licenses**.
- **Facility & Multi-Site Management:** Track multiple customer properties, facility types (Healthcare, F&B, Industrial, Residential), square footage, and risk ratings.
- **Annual Maintenance Contracts (AMC):** Manage recurring service agreements, scopes of treatment, billing cycles (Monthly, Quarterly, Upfront), and renewal pipelines.
- **Chemical & Consumable Tracking:** Log specific active ingredients, batch numbers, dosage, and consumption per visit.
- **Bi-Directional HR Attendance Sync:** Automatically marks technician attendance as `Present` in Frappe HR upon work order completion.
- **Rich Dashboard & Operations Workspace:** Built-in number cards, quick navigation shortcuts, and 8+ analytical reports.
- **Pest Service Certificate:** Ready-to-print digital compliance and completion certificate for client handover.

---

## System Architecture & Lifecycle

```
[ Customer & Client Site ] 
          │
          ├──> [ Pest Control Contract (AMC) ] 
          │                 │
          │                 ▼
          └───> [ Pest Work Order ] (PWO-.YYYY.-)
                        │
                        ▼
          [ Smart Allocation Engine (api.py) ]
          ├── Checks: Double Booking Conflicts
          ├── Checks: Frappe HR Leave Records
          ├── Checks: Company Holiday / Weekly Off List
          └── Checks: Pesticide License Validity
                        │
                        ▼
          [ Manpower Allocation ] (MPA-.YYYY.-)
                        │
                        ▼
          [ Field Execution & Chemical Usage ]
                        │
                        ▼
          [ Work Order Closure & Sign-Off ]
          ├── Client Feedback & Quality Review
          ├── Service Certificate Generation
          └── Auto-Sync: Frappe HR Attendance Ledger (Present)
```

---

## Core Modules & DocTypes

### 1. Operations & Work Orders
* **Pest Work Order (`Pest Work Order`):** Central operational document representing a scheduled field visit.
  - Naming Series: `PWO-.YYYY.-`
  - Links to Customer, Client Site, AMC Contract, and Service Type.
  - Multi-technician allocation child table (`Pest Work Order Technician`).
  - Applied chemicals and consumable materials table (`Pest Chemical Consumable`).
  - Digital feedback capture: Client rating, technician observations, and supervisor quality notes.

### 2. Smart Manpower Allocation Engine
* **Manpower Allocation (`Manpower Allocation`):** Star submittable document managing technician assignments to jobs.
  - Naming Series: `MPA-.YYYY.-`
  - Shift Slots: `Morning (08:00 - 12:00)`, `Afternoon (13:00 - 17:00)`, `Evening/Night (18:00 - 22:00)`.
  - Roles: `Lead Technician`, `Assistant Technician`, `Chemical Sprayer`, `Quality Inspector`.
  - Check-in & Check-out timestamp recording.
  - Automated triggers to link back to the Work Order and update HR Attendance.

### 3. Facility & Contract Management
* **Pest Control Site (`Pest Control Site`):** Stores customer premises details.
  - Supports multiple sites per client.
  - Site Types: Commercial Office, Residential Villa / Flat, Food & Beverage / Restaurant, Healthcare / Hospital, Industrial / Warehouse, Shopping Mall.
  - Risk categorization: Low, Medium, High, Critical - Food Safety.
* **Pest Control Contract (`Pest Control Contract`):**
  - Contract Types: Annual Maintenance Contract (AMC), One-Time Service Contract, Seasonal Disinfestation.
  - Tracks total contract amount, payment schedule, and recurring service frequencies.
* **Service Type (`Service Type`):** Catalog of treatments (e.g., Termite Control, Bedbug Eradication, Rodent Baiting, General Disinfection, Mosquito Fogging).

---

## HR & ERPNext Integrations

| Module / DocType | Integration Touchpoint | Business Rule Enforced |
| :--- | :--- | :--- |
| **Employee** | Link on Manpower Allocation | Fetches technician contact, certification, and license status. |
| **Leave Application** | Frappe HR Leave Validation | Blocks scheduling if technician is on approved leave. |
| **Holiday List** | Company Holiday Validation | Warns / blocks assignment on weekly offs and public holidays. |
| **Shift Assignment** | Frappe HR Shifts | Correlates shift hours with dispatch time slots. |
| **Attendance** | Auto-Mark Present | Submits attendance record in HR ledger on work order closure. |
| **Customer** | CRM / Selling | Synchronizes customer contacts and billing addresses. |
| **Item** | Stock & Consumables | Chemical items and PPE equipment linking for inventory tracking. |

---

## Reports & Executive Dashboard

The custom **Pest Control & FM Workspace** includes:

### Operational KPI Number Cards:
1. **Scheduled Jobs:** Real-time count of pending / upcoming jobs.
2. **Completed Jobs:** Closed work orders for the current operational cycle.
3. **Active AMC Contracts:** Running customer maintenance contracts.
4. **Certified Technicians:** Active licensed technicians ready for deployment.

### Standard Analytical Reports:
* **Today's Dispatch Report:** Live morning standup sheet for field supervisors.
* **Daily Manpower Deployment:** Technician allocation matrix sorted by shift and role.
* **Overdue AMC Visits:** Alerts for contracts overdue for periodic maintenance.
* **Technician Planned Deployment vs Recorded Attendance:** Audit variance between dispatched shifts and HR check-ins.
* **Failed Services & Revisit Queue:** Tracks unresolved customer complaints and rework tickets.
* **Scheduled & Unallocated Work Orders:** Identifies scheduled jobs lacking manpower.
* **Work Orders in Progress:** Active on-site jobs.
* **Completed Visits by Date:** Historical audit log of completed visits.
* **AMC Contract Expiry & Renewal:** Forward-looking renewal pipeline for commercial accounts.

---

## Whitelisted REST APIs

The app exposes REST endpoints for integration with mobile apps, client portals, and external dispatch tools (`pest_control/api.py`):

### 1. `get_available_technicians`
Finds eligible technicians for a given date and time slot:
```python
frappe.call({
    method: "pest_control.api.get_available_technicians",
    args: {
        date: "2026-10-26",
        time_slot: "Morning (08:00 - 12:00)"
    }
});
```
*Filters out technicians who are on approved leave or already booked, and scores them by completed jobs.*

### 2. `assign_technicians`
Bulk creates and submits `Manpower Allocation` records for a work order:
```python
frappe.call({
    method: "pest_control.api.assign_technicians",
    args: {
        work_order: "PWO-2026-00001",
        assignments: [
            {"employee": "EMP-0001", "role": "Lead Technician"},
            {"employee": "EMP-0002", "role": "Chemical Sprayer"}
        ]
    }
});
```

### 3. `complete_work_order`
Completes a work order, updates technician check-out timestamps, and registers HR attendance:
```python
frappe.call({
    method: "pest_control.api.complete_work_order",
    args: {
        work_order: "PWO-2026-00001",
        client_feedback: "Excellent",
        remarks: "Cockroach gel baiting applied across kitchen and pantry."
    }
});
```

---

## Installation Guide

### Prerequisites
- [Bench CLI](https://github.com/frappe/bench) installed
- Python 3.10+
- Frappe Framework v15
- ERPNext v15
- Frappe HR v15

### Step-by-Step Installation

1. Navigate to your frappe-bench directory:
   ```bash
   cd ~/frappe-bench
   ```

2. Download the app repository:
   ```bash
   bench get-app https://github.com/Gopika-Dileep/frappe-custom-app.git pest_control
   ```

3. Install the app on your site:
   ```bash
   bench --site <your-site-name> install-app pest_control
   ```

4. Run database migrations and clear cache:
   ```bash
   bench --site <your-site-name> migrate
   bench --site <your-site-name> clear-cache
   ```

5. (Optional) Run test engine validation:
   ```bash
   bench --site <your-site-name> execute pest_control.test_engine.run_test
   ```

---

## Development & Code Quality

This project adheres to strict Frappe community standards and uses `pre-commit` hooks for linting and code formatting:

```bash
cd apps/pest_control
pre-commit install
```

Configured Linters & Tools:
- **Ruff:** Lightning-fast Python linting and formatting.
- **ESLint & Prettier:** JavaScript formatting for desk views and client scripts.
- **Pyupgrade:** Modern Python syntax enforcement.
- **Frappe Semgrep:** Security and best practice rule scanning.

---

## License & Author

- **Author:** Gopika Dileep ([@Gopika-Dileep](https://github.com/Gopika-Dileep))
- **Email:** gopikadileep76@gmail.com
- **License:** MIT License ([license.txt](license.txt))
