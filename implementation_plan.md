# Fenix IT Mall – Django Implementation Plan

## Overview

A production-quality **IT Shop Management & Stock Management System** built with Django 5, SQLite, Tailwind CSS, Alpine.js, Three.js, GSAP, and Chart.js. This is a BCA final-year project that must look like a premium commercial SaaS product.

---

## Architecture Summary

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 5, SQLite |
| ORM | Django ORM (no raw SQL) |
| Image | Pillow |
| PDF | ReportLab |
| Frontend CSS | Tailwind CSS (CDN) |
| Frontend JS | Alpine.js, Three.js, GSAP, Chart.js |
| Auth | Django built-in auth + custom extension |

---

## Django Apps Structure

```
fenix_it_mall/          ← Django project root
├── fenix_it_mall/      ← settings, urls, wsgi
├── core/               ← base templates, context processors, utilities
├── accounts/           ← auth: login, register, profile, roles
├── dashboard/          ← dashboard cards, charts, recent activity
├── products/           ← product CRUD, barcode, QR, images
├── inventory/          ← stock in/out, low stock, adjustments
├── sales/              ← sales invoice, POS, print/PDF
├── purchase/           ← purchase orders, receive stock, payments
├── customers/          ← customer profiles, purchase history, rewards
├── suppliers/          ← supplier profiles, purchase history
├── employees/          ← employee profiles, attendance, salary
├── reports/            ← all reports, export PDF/CSV
├── notifications/      ← toast, system, low-stock alerts
└── settings_app/       ← company settings, theme, backup
```

---

## Proposed Changes (Module by Module)

### Phase 1 – Project Setup & Core

#### [NEW] Project scaffold
- Run `django-admin startproject fenix_it_mall .`
- Create all 13 apps via `manage.py startapp`
- Configure `settings.py`: INSTALLED_APPS, MEDIA, STATIC, AUTH, TEMPLATES

#### [NEW] `fenix_it_mall/settings.py`
- SQLite database config
- Tailwind CDN via templates
- Media/static roots
- Login redirect URLs
- Custom user model pointer

#### [NEW] `core/` app
- `base.html` – master template with sidebar, navbar, footer
- `landing.html` – Three.js hero page
- `403.html`, `404.html`, `500.html`
- Context processors for notifications, settings
- Utility functions (barcode gen, QR gen, PDF helpers)

---

### Phase 2 – Authentication & User Roles

#### [NEW] `accounts/models.py`
- `CustomUser` extending `AbstractUser`
- Fields: role (Admin/Manager/Employee/Cashier), profile_picture, phone, address
- Role-based permission mixin

#### [NEW] `accounts/` templates
- `login.html` – Glassmorphism login card
- `register.html`
- `forgot_password.html`
- `profile.html` + `edit_profile.html`
- `change_password.html`

---

### Phase 3 – Dashboard

#### [NEW] `dashboard/views.py`
- Stats aggregation (products, sales today, revenue, low stock, etc.)
- Chart data API endpoints (JSON for Chart.js)

#### [NEW] `dashboard/templates/dashboard/index.html`
- 10 animated stat cards
- Monthly sales line chart
- Pie chart for categories
- Recent activities table
- Quick action buttons

---

### Phase 4 – Products, Categories, Brands

#### [NEW] `products/models.py`
- `Category`: name, slug, image, description
- `Brand`: name, logo, description
- `Product`: all fields (name, code, barcode, QR, images, price, GST, warranty, stock, status, etc.)
- `ProductImage`: multiple images per product

#### [NEW] Product templates
- List with search/filter/sort/pagination
- Detail view with image gallery
- Add/Edit form with live preview
- Delete confirmation modal

---

### Phase 5 – Inventory

#### [NEW] `inventory/models.py`
- `StockMovement`: product, type (IN/OUT/ADJUST/DAMAGED/RETURN), quantity, reason, date
- Low stock threshold per product

#### [NEW] Inventory templates
- Current stock table
- Low stock alerts
- Stock in / stock out forms
- Stock history

---

### Phase 6 – Suppliers & Purchase

#### [NEW] `suppliers/models.py`
- `Supplier`: company, contact, phone, email, address, GST

#### [NEW] `purchase/models.py`
- `PurchaseOrder`: supplier, date, status, total
- `PurchaseItem`: order, product, qty, price
- `SupplierPayment`: order, amount, method, date

---

### Phase 7 – Customers & Sales / POS

#### [NEW] `customers/models.py`
- `Customer`: name, phone, email, address, reward_points

#### [NEW] `sales/models.py`
- `Sale`: customer, date, discount, GST, payment_method, total, invoice_no
- `SaleItem`: sale, product, qty, price

#### [NEW] POS System
- Barcode scanner input
- Dynamic cart (Alpine.js)
- Payment modal (Cash/UPI/Card)
- Print/PDF invoice (ReportLab)

---

### Phase 8 – Employees

#### [NEW] `employees/models.py`
- `Employee`: profile, designation, salary, status
- `Attendance`: employee, date, status
- `Leave`: employee, start, end, reason, status

---

### Phase 9 – Reports

#### [NEW] `reports/views.py`
- Sales report (date range filter)
- Purchase report
- Profit & loss
- Inventory status
- Export PDF (ReportLab)
- Export CSV (Django StreamingHttpResponse)

---

### Phase 10 – Notifications & Settings

#### [NEW] `notifications/models.py`
- `Notification`: type, message, is_read, timestamp
- Context processor injects unread count into all pages

#### [NEW] `settings_app/models.py`
- `CompanySettings`: singleton model
- Company name, logo, GST, invoice prefix, currency, theme

---

### Phase 11 – Static Assets & Animations

#### [NEW] `static/css/main.css`
- CSS variables for the color palette
- Glassmorphism utility classes
- Card hover lift animations
- Sidebar responsive collapse

#### [NEW] `static/js/three_hero.js`
- Three.js scene: floating 3D objects (laptop, keyboard, GPU, SSD)
- Particle system with RGB neon lights
- Mouse-interactive camera movement

#### [NEW] `static/js/dashboard.js`
- Chart.js initialisation for all dashboard charts
- GSAP counter animations for stat cards
- Animated gradient borders

#### [NEW] `static/js/pos.js`
- Barcode scanner listener
- Cart state management (Alpine.js store)
- Payment flow

---

### Phase 12 – Admin & Documentation

#### [NEW] Custom Django Admin
- Model admin for all apps
- Dashboard statistics panel
- Product image preview
- Filters and search on all models

#### [NEW] `README.md`
- Project overview, setup guide, features list

#### [NEW] `requirements.txt`
- `django>=5.0`, `pillow`, `reportlab`, `python-barcode`, `qrcode`

---

## Verification Plan

### Automated
```bash
python manage.py check          # Django system check
python manage.py migrate        # All migrations run cleanly
python manage.py createsuperuser  # Admin creation
python manage.py runserver      # Dev server starts
```

### Manual Verification
- Landing page Three.js animation visible
- Login/register flow works
- Dashboard charts load
- Product CRUD with image upload
- POS checkout generates PDF invoice
- Low stock notification appears
- PDF/CSV report export works
- Responsive sidebar collapses on mobile

---

## Execution Order (Phases)

| # | Phase | Estimated Complexity |
|---|-------|---------------------|
| 1 | Project setup + core + base template | High |
| 2 | Accounts + auth | Medium |
| 3 | Dashboard | High |
| 4 | Products + Categories + Brands | High |
| 5 | Inventory | Medium |
| 6 | Suppliers + Purchase | Medium |
| 7 | Customers + Sales + POS | Very High |
| 8 | Employees | Medium |
| 9 | Reports + Export | Medium |
| 10 | Notifications + Settings | Low |
| 11 | Static: Three.js, GSAP, Chart.js | High |
| 12 | Admin panel + README | Low |

> **Total estimated files: ~150+** across models, views, forms, urls, templates, static assets.
