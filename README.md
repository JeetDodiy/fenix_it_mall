# 🖥️ Fenix IT Mall — Enterprise POS & Inventory Management System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen.svg)](https://fenix-it-mall.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Tests](https://img.shields.io/badge/Tests-195%2F195%20Passed%20(100%25)-brightgreen.svg)]()
[![UI](https://img.shields.io/badge/UI-Glassmorphism%20CSS-cyan.svg)]()
[![Academic](https://img.shields.io/badge/Semester%205-College%20Project-orange.svg)]()

> A modern, full-featured **Point of Sale (POS)**, **Inventory Control**, and **Enterprise Resource Planning (ERP)** web application built specifically for computer hardware and electronics retail stores.

- **Developer / Student**: **[Jeet Dodiya](https://github.com/JeetDodiy)**
- **Academic Milestone**: **Semester 5 College Project Submission**
- **Live Cloud Website**: **[https://fenix-it-mall.onrender.com](https://fenix-it-mall.onrender.com)**

---

## ✨ Key Features

### 🛒 1. Advanced POS Terminal (Point of Sale)
- **High-Speed Checkout**: Keyboard-first shortcuts (`F2` search, `F8` hold, `F9` pay, `Esc` clear).
- **Streamlined Search Bar**: Clean flexbox badges (`SCAN` and `F2`) with generous padding to prevent text collision across all screen sizes.
- **Barcode Gun Scanner**: Automatic barcode listening with instant add-to-cart.
- **Glassmorphic Product Cards**: Unclipped cards displaying brand, title, SKU, stock count (`● X in stock`), price in ₹, and `+` add-to-cart button.
- **Category Rail**: Category filtering with custom uploaded thumbnails (`Cabinet`, `Laptop`) and contextual hardware SVG icons.
- **Cart & Split Payments**: Auto tax calculation (GST 18%), item discounts, and multi-method checkout (Cash, UPI, Card).
- **Hold Sale (F8)**: Suspend active transactions and resume anytime without data loss.
- **Thermal & A4 Invoices**: Instant printable bill/receipt generation.

### 📦 2. Inventory & Stock Engine
- **Duplicate Product Name Restriction**: Enforces unique product names at the database level (`unique=True`) and form level (`name__iexact`) to prevent duplicate items.
- **Direct Stock Procurement**: Purchase orders automatically credit stock to inventory without redundant receiving steps.
- **Live Stock Movements**: Every transaction (sales, purchases, returns) logs previous and updated quantities with timestamped references.
- **Low Stock Alerts**: Real-time automated notifications when stock drops below threshold.
- **Barcode & QR Generation**: Printable Code128 barcodes and 2D QR codes generated on-the-fly for every product.

### 🏢 3. Supplier Bill & Payment Report
- **Supplier Ledger**: Comprehensive tracking of total bills, payments given, and outstanding dues.
- **Sequential PO Numbering**: Year-based sequential series (`PO-26-01`, `PO-26-02`, etc.) with automatic year rollover.
- **Bill Number Tracking**: Records supplier invoice numbers (e.g. `AS-8859`) alongside internal PO numbers.
- **Interactive Multi-Filter**: Filter by Supplier, Payment Status (`Fully Paid`, `Partial`, `Unpaid`), Date Range, and Search Query.
- **Expandable Drawers**: View itemized bill breakdowns (Qty, Unit Rate, Subtotal) and installment payment histories.
- **1-Click Export**: Download reports in styled landscape **PDF** or spreadsheet **CSV**.

### 🧾 4. Sequential Sales Invoicing
- **Year-Based Invoice Series**: Clean, sequential invoice numbering (`INV-26-01`, `INV-26-02`, ..., `INV-26-15`) that rolls over automatically to `INV-27-01` in 2027.
- **Historical Audit Logs**: Complete invoice audit trail tracking customer name, line items, and payment methods.

### 👥 5. Customer CRM & Loyalty Points
- Complete profile management with purchase history and spending analytics.
- Automatic loyalty reward points accrued per rupee spent and redeemable at POS checkout.

### 👔 6. Employees & HR Management
- Unique auto-generated Employee ID (`EMP-XXXXXX`), designation, department, and salary.
- Daily attendance tracking (Present, Absent, Half-Day, Leave) with duplicate prevention per date.
- Leave application and manager approval workflows.

### 📊 7. Executive Financial Reports
- **Sales Reports**: Daily, monthly, and custom range sales metrics.
- **Profit & Loss**: Gross revenue, COGS (Cost of Goods Sold), and net margins.
- **Inventory Valuation**: Current asset value by cost price and retail price.

### 🎨 8. Design Aesthetics & Adaptive Splash Screen
- **Dark & Light Mode**: Curated dark-mode default with vibrant neon accents, plus 1-click **Light Theme** toggle.
- **Adaptive Splash Screen**: Automatically renders pure white in light mode and deep black/navy in dark mode.
- **Dynamic Company Logo**: Custom logo upload with live preview and persistent cloud media serving.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.10+ / Django 5.0.6 (MVT Architecture) |
| **Production Server** | Gunicorn WSGI + WhiteNoise static compression |
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

### 4. Apply Database Migrations & Seed Data
```bash
python manage.py migrate
python manage.py init_admin
python manage.py loaddata initial_catalog.json
```

### 5. Run the Development Server
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

## 🌐 Cloud Deployment (Render.com)

The project is deployed live on Render with automated GitHub CI/CD:
- **Live URL**: **`https://fenix-it-mall.onrender.com`**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn fenix_it_mall.wsgi:application`
- **Full Guide**: See [upoald_project.txt](upoald_project.txt) for step-by-step instructions.

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
├── Procfile           # Production WSGI process declaration
├── build.sh           # Cloud build, migration & seed script
├── render.yaml        # Render 1-click blueprint configuration
├── upoald_project.txt # Complete deployment guide for Render
├── Finaly_doc_project.md # Full academic project report (Semester 5)
├── requirements.txt   # Python package dependencies
├── manage.py          # Django management script
└── test_all_195_cases.py # 195/195 automated test suite
```

---

## 📜 License & Academic Disclosure
This project is developed as an academic submission for **Semester 5** by **Jeet Dodiya**. Open for educational and non-commercial portfolio evaluation.
