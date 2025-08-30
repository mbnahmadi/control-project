# Control project system

## Overview
A Django-based **internal project monitoring system** (no public users).  
Admins create and maintain projects in **Django Admin**, can **filter by company, locations, date range**, and can **export to Excel**.  
Senior managers can **view locations on a map (Leaflet)** and query data through simple APIs (active/all locations, activity by date range, etc.).

---

## Features

### Admin & Data Entry
- Create/manage **Companies**, **Day Formats**, and **Projects**
- Strong validation in `clean()` and computed fields in `save()`:
  - `total_days`, `total_cycle`, and `is_active_now`
- **Import/Export to Excel** with `django-import-export`
- Advanced list filters with **date range** (via `django-admin-rangefilter`)
- Read-only computed fields in admin: `total_days`, `total_cycle`, `is_active_now`

### Project Tracking
- Active project detection via custom manager: `ProjectModel.active_locations`
- Inclusive day counting between `start_date` and `end_date`
- Cycle math: supports `start_cycle`/`end_cycle` (2 cycles/day)

### Manager Access (Read-Only)
- **Map integration (Leaflet)** to visualize active/all points
- **APIs** for:
  - Active locations
  - All locations
  - Company/location activity summaries in a given date range
  - Download latest project PDF (if location is active)

### Feedback Module
- Record employer **feedback per project**
- Admin **responses** with optional file attachments (e.g., ISO forms)

---

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Admin Tools:** django-import-export, django-admin-rangefilter
- **DB:** PostgreSQL (recommended)
- **Frontend Integration:** Leaflet.js (separate frontend)
- **Storage:** Local `FileField` for PDFs and attachments

---

## Data Model (Key Entities)
- **CompanyModel**: `name`
- **DayFormatModel**: `format_name`
- **ProjectModel**:
  - `company_name (FK)`, `location`, `lat`, `lon`, `description`, `image_description`
  - `start_date`, `end_date`, `start_cycle`, `end_cycle`, `days_format (FK)`
  - Computed: `total_days`, `total_cycle`, `is_active_now`
  - `latest_pdf_path` for report downloads
  - Managers: `objects` (all), `active_locations` (only active ones)

- **FeedBackModel**:
  - `project (FK)`, `name`, `phone_number`, `through`, `date`, `message`

- **FeedBackResponseModel**:
  - `feedback (OneToOne)`, `through`, `date`, `message`
  - `attachment`, `iso_form` (file uploads)

---

## How “Active Days” Are Calculated
For a given query range `[start, end]`:
- Overlap is computed with each project’s `[start_date, end_date or end]`
- If `end_date` is `NULL`, it’s treated as `end` for the overlap
- `active_days = (overlap_end - overlap_start) + 1` (inclusive)


## In Progress / Upcoming Features:

- **Total Days Calculation per Company**:  
  Currently, the system calculates the number of days a company has data within a selected date range. In upcoming versions, an additional feature will be added to calculate the **total number of days each company has recorded data** (regardless of the selected range).  
  > This logic will be implemented at the database level to ensure better performance and efficiency.

- **Ongoing Development**:  
  This project is still under active development, and more improvements and new features will be added over time.

---
## Installation & Setup
```bash
# Clone
git clone https://github.com/mbnahmadi/control-project.git
cd control-project

# Install
pip install -r requirements.txt

# Migrate
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run dev server
python manage.py runserver
```