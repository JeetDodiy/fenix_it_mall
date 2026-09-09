# 🖥️ Fenix IT Mall — Enterprise POS & Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Tests](https://img.shields.io/badge/Tests-195%2F195%20Passed%20(100%25)-brightgreen.svg)]()
[![UI](https://img.shields.io/badge/UI-Glassmorphism%20CSS-cyan.svg)]()
[![Academic](https://img.shields.io/badge/Semester%205-College%20Project-orange.svg)]()

> A modern, full-featured **Point of Sale (POS)**, **Inventory Control**, and **Enterprise Resource Planning (ERP)** web application built specifically for computer hardware and electronics retail stores.

Developed by **[Jeet Dodiya](https://github.com/JeetDodiy)** for **Semester 5 Project Submission**.

---

## ✨ Key Features

### 🛒 1. Advanced POS Terminal (Point of Sale)
- **High-Speed Checkout**: Keyboard-first shortcuts (`F2` search, `F8` hold, `F9` pay, `Esc` clear).
- **Barcode Gun Scanner**: Automatic barcode listening with instant add-to-cart.
- **Glassmorphic Product Cards**: Unclipped cards displaying brand, title, SKU, stock count (`● X in stock`), price in ₹, and `+` add-to-cart button.
- **Category Rail**: Category filtering with custom uploaded thumbnails (`Cabinet`, `Laptop`) and contextual hardware SVG icons.
- **Cart & Split Payments**: Auto tax calculation (GST 18%), item discounts, and multi-method checkout (Cash, UPI, Card).
- **Hold Sale (F8)**: Suspend active transactions and resume anytime without data loss.
- **Thermal & A4 Invoices**: Instant printable bill/receipt generation.

### 📦 2. Inventory & Stock Engine
- **Direct Stock Procurement**: Purchase orders automatically credit stock to inventory without redundant receiving steps.
- **Live Stock Movements**: Every transaction (sales, purchases, returns) logs previous and updated quantities with timestamped references.
- **Low Stock Alerts**: Real-time automated notifications when stock drops below threshold.
- **Barcode & QR Generation**: Printable Code128 barcodes and 2D QR codes generated on-the-fly for every product.

### 🏢 3. Supplier Bill & Payment Report
- **Supplier Ledger**: Comprehensive tracking of total bills, payments given, and outstanding dues.
- **Bill Number Tracking**: Records supplier invoice numbers (e.g. `INV-8859`) alongside internal PO numbers.
- **Interactive Multi-Filter**: Filter by Supplier, Payment Status (`Fully Paid`, `Partial`, `Unpaid`), Date Range, and Search Query.
- **Expandable Drawers**: View itemized bill breakdowns (Qty, Unit Rate, Subtotal) and installment payment histories.
- **1-Click Export**: Download reports in styled landscape **PDF** or spreadsheet **CSV**.

### 👥 4. Customer CRM & Loyalty Points
- Complete profile management with purchase history and spending analytics.
- Automatic loyalty reward points accrued per rupee spent and redeemable at POS checkout.

### 👔 5. Employees & HR Management
- Unique auto-generated Employee ID (`EMP-XXXXXX`), designation, department, and salary.
- Daily attendance tracking (Present, Absent, Half-Day, Leave) with duplicate prevention per date.
- Leave application and manager approval workflows.

### 📊 6. Executive Financial Reports
- **Sales Reports**: Daily, monthly, and custom range sales metrics.
- **Profit & Loss**: Gross revenue, COGS (Cost of Goods Sold), and net margins.
- **Inventory Valuation**: Current asset value by cost price and retail price.

### 🎨 7. Design Aesthetics & Theme Switcher
- Curated dark-mode default with vibrant neon accents (cyan, purple, emerald).
- 1-click **Light Theme** toggle with persistent local storage state.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.10+ / Django 5.0.6 (MVT Architecture) |
| **Database** | SQLite3 (Persistent, zero-configuration) |
| **Frontend Styling** | Vanilla CSS3 (Custom Glassmorphism System, No Tailwind) |
| **Reactive Client** | Alpine.js 3.x (Lightweight reactive state) |
| **Document Generation**| ReportLab (PDF) & Python `csv` module |
| **Barcodes & QR** | `python-barcode` (Code128/EAN-13) & `qrcode` |
| **Security** | Django CSRF, ORM parameterized queries, XSS protection, RBAC |

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/JeetDodiy/fenix_it_mall.git
cd fenix_it_mall
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Collect Static Files (Optional for production)
```bash
python manage.py collectstatic --noinput
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser!

---

## 🔑 Default Login Credentials

| Role | Username | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | Full system access across all modules & settings |
| **Manager** | `manager` | `manager123` | Inventory, purchases, supplier payments, reports |
| **Cashier** | `cashier` | `cashier123` | POS terminal checkout only |
| **Employee** | `emp_rahul` | `emp123` | Personal attendance and salary log |

---

## 🧪 Automated Testing & Verification

The project includes an exhaustive automated test suite covering 195 test cases across all modules, edge cases, RBAC permissions, and end-to-end business workflows:

```bash
python test_all_195_cases.py
```

### Test Results:
```text
================================================================================
  195 TEST CASES EXHAUSTIVE VERIFICATION SUMMARY
================================================================================
Total Test Cases Evaluated : 195
Passed                     : 195 (100.0%)
Failed                     : 0
================================================================================
```

---

## 🌐 Free Hosting / Deployment Guide

### Option 1: PythonAnywhere (Recommended for College Viva)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Open a **Bash console** and clone your repo:
   ```bash
   git clone https://github.com/JeetDodiy/fenix_it_mall.git
   cd fenix_it_mall
   python3.10 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python manage.py collectstatic --noinput && python manage.py migrate
   ```
3. Configure the **Web Tab**:
   - Python 3.10 manual configuration
   - Virtualenv: `/home/<username>/fenix_it_mall/venv`
   - Static mapping: `/static/` → `/home/<username>/fenix_it_mall/static`
   - Media mapping: `/media/` → `/home/<username>/fenix_it_mall/media`
4. Update WSGI file and reload!

### Option 2: Render.com
1. Connect your GitHub repo to [render.com](https://render.com).
2. Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. Start Command: `gunicorn fenix_it_mall.wsgi:application`

---

## 📁 Project Structure

```text
fenix_it_mall/
├── accounts/          # Custom user model & authentication
├── core/              # Global views, context processors & utilities
├── customers/         # Customer CRM & loyalty points
├── dashboard/         # Executive KPIs, revenue charts & activity logs
├── employees/         # Employee profiles, attendance & leaves
├── inventory/         # Stock management & audit movement logs
├── notifications/     # Real-time stock alerts & toasts
├── products/          # Products, categories, brands, barcode & QR
├── purchase/          # Purchase orders, bill tracking & supplier payments
├── reports/           # Financial analytics & Supplier Bill reports
├── sales/             # POS terminal, invoicing & checkout logic
├── settings_app/      # Company settings & rebranding
├── static/            # Glassmorphism CSS design system & JavaScript
├── templates/         # Semantic HTML5 / DTL templates
├── media/             # Uploaded product & category images
├── Finaly_doc_project.md # Full academic project report
├── requirements.txt   # Python package dependencies
├── manage.py          # Django management script
└── test_all_195_cases.py # 195/195 automated test suite
```

---

## 📜 License & Academic Disclosure
This project is developed as an academic submission for **Semester 5** by **Jeet Dodiya**. Open for educational and non-commercial portfolio evaluation.
