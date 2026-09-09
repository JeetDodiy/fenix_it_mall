# Fenix IT Mall — Enterprise POS & Inventory Management System
## Final Project Documentation (Academic Semester 5)

---

### Executive Summary
**Fenix IT Mall** is a comprehensive, production-grade Point of Sale (POS), Inventory Control, and Enterprise Resource Planning (ERP) web application developed specifically for computer hardware, peripheral, and IT electronics retailers. The system streamlines retail checkout, stock procurement with instant ledger updates, supplier bill and payment reconciliation, customer relationship tracking, employee HR/attendance, and executive financial reporting within a modern glassmorphic interface.

- **Developer / Student**: Jeet Dodiya
- **Academic Milestone**: Semester 5 College Project
- **GitHub Repository**: [https://github.com/JeetDodiy](https://github.com/JeetDodiy)
- **Test Coverage**: 195 / 195 Automated Test Cases Passed (100.0%)

---

## 1. Technology Stack & System Architecture

### 1.1 Backend Core
- **Framework**: Python 3.10+ with Django 5.0.6
- **Architecture**: Model-View-Template (MVT) with modular Django apps
- **Database**: SQLite3 (persistent local and production hosting compatible)
- **Security**: Django CSRF Protection, parameterized ORM against SQL Injection, XSS auto-escaping, password hashing with PBKDF2/SHA256, and Role-Based Access Control (RBAC).

### 1.2 Frontend & UI/UX
- **Markup & Templates**: Semantic HTML5 with Django Template Language (DTL)
- **Styling**: Vanilla CSS3 design system featuring custom Dark & Light themes, backdrop blurs, dynamic glow borders, micro-animations, and full responsive grid layouts.
- **Reactive UI**: Alpine.js for real-time POS interactions, search filtering, and held-cart state management without heavy frontend frameworks.
- **Documents & Export**: ReportLab for formatted PDF generation; Python `csv` module for tabular exports; `python-barcode` & `qrcode` for automated product code generation.

---

## 2. Core Functional Modules

### 2.1 Authentication & Role-Based Access Control (RBAC)
- **Roles**:
  - **Admin / Superuser**: Full system access across all modules, settings, employee management, and order deletions.
  - **Manager**: Catalog management, purchase orders, supplier payments, stock adjustments, and business analytics.
  - **Cashier**: Restricted strictly to POS terminal checkout and viewing product catalogs.
  - **Employee**: Limited to viewing own attendance, salary records, and applying for leaves.
- **Session & Security**: Secure session tokens, password change workflows, and forced login guards on all business routes.

### 2.2 Product Catalog & Inventory
- **Hierarchy**: Products linked to Categories and Brands.
- **Image Support**: Multi-image uploads for products, dedicated thumbnail logos for categories and brands.
- **Codes & Automation**: Auto-generated SKU codes (`FIM-XXXXXXXX`) and automated EAN-13 barcode numbers. Direct generation of printable Code128 barcodes and 2D QR codes.
- **Inventory Engine**: Real-time stock counts, minimum threshold notifications, and atomic stock movements (`movement_type: in, out, adjustment`).

### 2.3 POS Terminal (Point of Sale)
- **Live Search & Barcode Scan**: Real-time keyboard-driven search (`F2` search, barcode scanner gun listener with automatic Enter submission).
- **Responsive Product Cards**: Clean 290px cards displaying image, brand, title, SKU, stock dot, price (`₹`), and quick `+` Add to Cart button with zero clipping.
- **Category Rail**: Quick category switching with custom thumbnail images and contextual hardware icons.
- **Cart Engine**: Real-time quantity adjustments, custom item discounts, overall GST (18%) calculation, and split payment modes (Cash, UPI, Card).
- **Hold Sale Feature**: Suspend ongoing sales with `F8` and resume instantly from local storage cache.
- **Checkout & Direct Receipt**: Instant stock decrement via database transaction lock and generation of clean, printable A4/thermal receipts.

### 2.4 Purchases & Direct Stock Procurement
- **Purchase Orders**: Create POs linked to registered suppliers with itemized cost prices and tax rates.
- **Direct Stock Addition**: Eliminates redundant multi-step receiving; stock is immediately credited to available inventory upon PO creation.
- **Bill Number Tracking**: Records supplier bill/invoice numbers (e.g. `INV-9821`) alongside system PO codes.
- **Payment Reconciliation**: Multi-installment payments (Cash, Bank Transfer, UPI, Cheque), partial payment tracking, and dynamic pending balance updates.

### 2.5 Supplier Bill & Payment Report
- **Dedicated Ledger**: Complete visibility into supplier purchases, payments given, and pending balances.
- **Interactive Multi-Filter**: Filter by Supplier, Payment Status (`Fully Paid`, `Partially Paid`, `Unpaid`), Date Range, and Search Query.
- **Expandable Drawers**: Click any bill row to inspect purchased items (quantity, unit rate, subtotal) and given payment history with dates and transaction methods.
- **Export Actions**: 1-click export to styled landscape PDF or complete spreadsheet CSV.

### 2.6 Customer CRM
- **Customer Profiles**: Name, unique phone number, email, address, and purchase logs.
- **Loyalty Program**: Automatic reward points accrual per rupee spent, redeemable at checkout.

### 2.7 Employees & HR Suite
- **Employee Records**: Unique auto-generated Employee ID (`EMP-XXXXXX`), designation, department, and salary.
- **Daily Attendance**: Mark Present, Absent, Half-Day, or Leave with duplicate entry prevention per calendar day.
- **Leave Management**: Leave requests with workflow for Manager/Admin approvals and balance deduction.

### 2.8 Business Reports & Analytics
- **Sales Analytics**: Daily, monthly, and custom date range sales metrics with PDF/CSV exports.
- **Profit & Loss**: Gross revenue, COGS (Cost of Goods Sold), operating expenses, and net profit margins.
- **Inventory Valuation**: Total inventory units and asset valuation by cost and retail value.

---

## 3. Database Schema Overview

```
CustomUser (AbstractUser)
  ├── is_admin, is_manager, is_cashier, is_employee
  └── phone, profile_picture

Category
  ├── name, slug, image, description, is_active

Brand
  ├── name, logo, website, description, is_active

Product
  ├── name, product_code (unique), barcode_number (unique)
  ├── category (FK), brand (FK), supplier (FK)
  ├── purchase_price, selling_price, gst_percentage
  ├── stock_quantity, low_stock_threshold
  └── barcode_image, qr_code, status, is_active

ProductImage
  └── product (FK), image, is_primary

PurchaseOrder
  ├── order_number (unique), bill_number, supplier (FK)
  ├── order_date, total_amount, paid_amount, status
  └── created_by (FK)

PurchaseOrderItem
  └── purchase_order (FK), product (FK), quantity, purchase_price, total_price

SupplierPayment
  └── purchase_order (FK), amount, payment_date, payment_method, note

Sale
  ├── invoice_number (unique), customer (FK), created_by (FK)
  ├── subtotal, discount_amount, gst_amount, grand_total
  ├── amount_paid, change_amount, payment_method, status
  └── created_at

SaleItem
  └── sale (FK), product (FK), quantity, unit_price, total_price

StockMovement
  ├── product (FK), movement_type (in/out/adj), quantity
  ├── quantity_before, quantity_after, reference, created_by (FK)
  └── created_at

Employee
  ├── employee_id (unique), user (FK), full_name, email, phone
  └── designation, department, salary, joining_date

Attendance
  └── employee (FK), date, status (present/absent/half_day/leave)

Leave
  └── employee (FK), leave_type, start_date, end_date, status, approved_by (FK)

CompanySettings (Singleton)
  ├── company_name, email, phone, address, gst_number
  └── logo, currency_symbol, default_tax_rate, theme_mode
```

---

## 4. Automated Verification & Test Results

A full enterprise test suite (`test_all_195_cases.py`) was executed against all functional specifications, edge cases, data boundaries, and role permissions.

### Test Results Summary
- **Total Test Cases Evaluated**: 195
- **Passed**: 195 (100.0%)
- **Failed**: 0
- **Pass Rate**: 100.0%

| Module Category | Test Case IDs | Count | Status |
| :--- | :--- | :--- | :--- |
| Core & Navigation | TC-CORE-001 – TC-CORE-007 | 7 | ✅ Passed |
| Authentication & RBAC | TC-AUTH-001 – TC-AUTH-009 | 9 | ✅ Passed |
| Dashboard Analytics | TC-DASH-001 – TC-DASH-006 | 6 | ✅ Passed |
| Products & Catalog | TC-PROD-001 – TC-PROD-012 | 12 | ✅ Passed |
| Categories & Brands | TC-CAT-001 – TC-BRD-006 | 12 | ✅ Passed |
| Barcodes & QR Codes | TC-BAR-001 – TC-BAR-007 | 7 | ✅ Passed |
| Inventory & Stock | TC-INV-001 – TC-INV-010 | 10 | ✅ Passed |
| POS Checkout & Sales | TC-POS-001 – TC-SALE-010 | 20 | ✅ Passed |
| Purchases & Suppliers | TC-PUR-001 – TC-PUR-013 | 13 | ✅ Passed |
| Customers CRM | TC-CUST-001 – TC-CUST-007 | 7 | ✅ Passed |
| Suppliers Module | TC-SUPP-001 – TC-SUPP-005 | 5 | ✅ Passed |
| Employees & HR | TC-EMP-001 – TC-EMP-LEV-005 | 16 | ✅ Passed |
| Reports & Supplier Ledger | TC-RPT-001 – TC-RPT-017 | 17 | ✅ Passed |
| Notifications & Alerts | TC-NOTIF-001 – TC-NOTIF-006 | 6 | ✅ Passed |
| Company Settings | TC-SET-001 – TC-SET-006 | 6 | ✅ Passed |
| UI/UX Glassmorphism | TC-UI-001 – TC-UI-013 | 13 | ✅ Passed |
| Security & SQLi/XSS | TC-SEC-001 – TC-SEC-008 | 8 | ✅ Passed |
| Edge Cases & Boundaries | TC-EDGE-001 – TC-EDGE-010 | 10 | ✅ Passed |
| Data Integrity & Unique Keys | TC-DATA-001 – TC-DATA-010 | 10 | ✅ Passed |
| End-to-End Enterprise Workflows | TC-E2E-001 – TC-E2E-007 | 7 | ✅ Passed |

---

## 5. Deployment & Free Hosting Guide

### Option A: PythonAnywhere (Recommended for College Submission)
1. **Create Free Account**: Register at [pythonanywhere.com](https://www.pythonanywhere.com).
2. **Open Bash Console**: Clone or upload project:
   ```bash
   git clone https://github.com/JeetDodiy/fenix_it_mall.git
   cd fenix_it_mall
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
3. **Configure Web Tab**:
   - Environment: Python 3.10
   - Source directory: `/home/<username>/fenix_it_mall`
   - Virtualenv: `/home/<username>/fenix_it_mall/venv`
   - Static mapping: `/static/` → `/home/<username>/fenix_it_mall/static`
   - Media mapping: `/media/` → `/home/<username>/fenix_it_mall/media`
4. **Reload**: Live at `https://<username>.pythonanywhere.com`.

### Option B: Render.com (GitHub CI/CD Deploy)
1. Create Web Service on [render.com](https://render.com) linked to your GitHub repo.
2. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start Command: `gunicorn fenix_it_mall.wsgi:application`

---

## 6. Default Demo Credentials

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | Full access across all modules |
| **Manager** | `manager` | `manager123` | Inventory, purchases, supplier payments, reports |
| **Cashier** | `cashier` | `cashier123` | POS terminal checkout only |
| **Employee** | `emp_rahul` | `emp123` | Attendance and personal salary log |
