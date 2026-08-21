# 📁 Fenix IT Mall — Project Documentation

> **Full-stack IT Shop Management System**  
> Built with Django 5.0.6 | SQLite | Vanilla CSS | JavaScript

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Django Apps (Modules)](#4-django-apps-modules)
5. [Database Models (ERD)](#5-database-models-erd)
6. [URL Route Map](#6-url-route-map)
7. [Static Assets](#7-static-assets)
8. [Templates Structure](#8-templates-structure)
9. [Configuration & Settings](#9-configuration--settings)
10. [Running the Project](#10-running-the-project)
11. [Role-Based Access Control](#11-role-based-access-control)

---

## 1. Project Overview

**Fenix IT Mall** is a comprehensive IT shop management system designed as a BCA final-year project. It provides end-to-end management for an IT hardware/software retail store, covering:

- Point of Sale (POS) — Barcode-driven billing with invoice generation
- Inventory Management — Real-time stock tracking with movement history
- Product Catalog — Categories, Brands, Barcodes & QR Codes auto-generated
- Reports & Analytics — Sales, purchase, profit, inventory, customers, suppliers, employees
- Customer & Supplier CRM — Contact tracking with purchase history
- Employee Management — Profiles, attendance, and leave management
- Notification System — Low-stock alerts, sale & purchase notifications
- Company Settings — Singleton settings for branding, GST, currency, theme

---

## 2. Technology Stack

| Layer            | Technology                                      |
|------------------|-------------------------------------------------|
| **Backend**      | Python 3.x, Django 5.0.6                        |
| **Database**     | SQLite 3 (`db.sqlite3`)                         |
| **Frontend**     | Vanilla HTML5, CSS3, JavaScript (ES6)           |
| **PDF Reports**  | ReportLab 4.2.2                                 |
| **Barcodes**     | python-barcode 0.15.1 (Code128)                 |
| **QR Codes**     | qrcode 7.4.2                                    |
| **Images**       | Pillow 10.3.0                                   |
| **Timezone**     | Asia/Kolkata (IST)                              |
| **Auth**         | Django Custom User Model (`accounts.CustomUser`)|

### Python Dependencies (`requirements.txt`)

```
Django==5.0.6
Pillow==10.3.0
reportlab==4.2.2
python-barcode==0.15.1
qrcode==7.4.2
```

---

## 3. Project Structure

```
finix_it_mall_demo_426/
|
|-- fenix_it_mall/           # Django project config
|   |-- settings.py          # All Django settings
|   |-- urls.py              # Root URL configuration
|   |-- wsgi.py              # WSGI entry point
|   `-- asgi.py              # ASGI entry point
|
|-- accounts/                # User authentication & management
|-- core/                    # Shared utilities & context processors
|-- dashboard/               # Main dashboard with analytics
|-- products/                # Product catalog (Category, Brand, Product)
|-- inventory/               # Stock movements & adjustments
|-- sales/                   # POS, billing & invoice
|-- purchase/                # Purchase orders from suppliers
|-- customers/               # Customer CRM
|-- suppliers/               # Supplier management
|-- employees/               # HR: employees, attendance, leaves
|-- reports/                 # Analytical reports (PDF, CSV)
|-- notifications/           # Notification system
|-- settings_app/            # Company-wide settings (singleton)
|
|-- templates/               # HTML templates
|   |-- base.html            # Master layout with sidebar & navbar
|   |-- accounts/
|   |-- dashboard/
|   |-- products/
|   |-- inventory/
|   |-- sales/
|   |-- purchase/
|   |-- customers/
|   |-- suppliers/
|   |-- employees/
|   |-- reports/
|   |-- notifications/
|   `-- settings_app/
|
|-- static/
|   |-- css/
|   |   |-- main.css          # Primary stylesheet (24KB)
|   |   |-- variables.css     # CSS design tokens
|   |   |-- layout.css        # Sidebar & layout structure
|   |   |-- dashboard.css     # Dashboard-specific styles
|   |   |-- forms.css         # Form input styles
|   |   |-- buttons.css       # Button components
|   |   |-- tables.css        # Table styles
|   |   |-- glass.css         # Glassmorphism effects
|   |   |-- animations.css    # Keyframe animations
|   |   |-- darkmode.css      # Dark mode overrides
|   |   `-- responsive.css    # Mobile responsive rules
|   `-- js/
|       |-- main.js           # Global utilities & toast messages
|       |-- dashboard.js      # Chart.js chart initialisation
|       |-- pos.js            # POS / billing logic
|       |-- sidebar.js        # Sidebar toggle
|       |-- modal.js          # Modal utilities
|       |-- theme.js          # Dark/Light theme switcher
|       `-- three_hero.js     # Three.js 3D hero animation (login page)
|
|-- media/                   # User-uploaded files (runtime)
|-- fixtures/                # Seed data (JSON fixtures)
|-- db.sqlite3               # SQLite database
|-- manage.py                # Django management CLI
`-- requirements.txt         # Python dependencies
```

---

## 4. Django Apps (Modules)

### 4.1 `accounts` App

**Purpose:** Custom user model with role-based access control (RBAC).

#### Model — `CustomUser` (extends `AbstractUser`)

| Field             | Type          | Notes                              |
|-------------------|---------------|------------------------------------|
| `username`        | CharField     | Inherited from AbstractUser        |
| `role`            | CharField     | `admin`, `manager`, `employee`, `cashier` |
| `phone`           | CharField     | Optional                           |
| `address`         | TextField     | Optional                           |
| `profile_picture` | ImageField    | Uploaded to `profiles/`            |
| `is_active`       | BooleanField  | Default: `True`                    |
| `created_at`      | DateTimeField | Auto-set on creation               |
| `updated_at`      | DateTimeField | Auto-updated                       |

**Properties:**
- `is_admin` — True if role is `admin` or `is_superuser`
- `is_manager` — True if role is `admin` or `manager`
- `is_cashier` — True if role is `admin`, `manager`, or `cashier`

#### Views & URLs

| URL                                     | View                         | Description                   |
|-----------------------------------------|------------------------------|-------------------------------|
| `/accounts/login/`                      | `login_view`                 | Login page                    |
| `/accounts/register/`                   | `register_view`              | Registration                  |
| `/accounts/logout/`                     | `logout_view`                | Logout                        |
| `/accounts/profile/`                    | `profile_view`               | Edit own profile              |
| `/accounts/password/`                   | `change_password`            | Change own password           |
| `/accounts/users/`                      | `user_list`                  | Admin: list all users         |
| `/accounts/users/add/`                  | `user_add`                   | Admin: add user               |
| `/accounts/users/<pk>/edit/`            | `user_edit`                  | Admin: edit user              |
| `/accounts/users/<pk>/change-password/` | `admin_change_user_password` | Admin: reset any password     |

---

### 4.2 `core` App

**Purpose:** Shared infrastructure — context processors that inject data globally into every template.

#### Context Processors

| Processor                 | Injects into context                            |
|---------------------------|-------------------------------------------------|
| `site_settings`           | `company_settings` — CompanySettings singleton  |
| `notifications_processor` | `unread_notifications_count`, `recent_notifications` |

---

### 4.3 `dashboard` App

**Purpose:** Main landing page post-login with KPI cards, charts, and recent activity.

#### Views

| URL                           | View               | Description                        |
|-------------------------------|--------------------|------------------------------------|
| `/dashboard/`                 | `index`            | Main dashboard with stats & charts |
| `/dashboard/chart-data/`      | `chart_data`       | AJAX endpoint for chart data       |
| `/dashboard/recent-activity/` | `recent_activity`  | Recent stock movements & sales     |

#### Dashboard KPIs
- Total Products, Categories, Brands
- Total Customers, Suppliers, Employees
- Today's Sales Count & Revenue
- Monthly Revenue, Sales Count & Profit
- Low Stock / Out of Stock / In Stock counts

#### Charts (via Chart.js)
- **Monthly Revenue & Profit** — last 6 months (line chart)
- **Category Distribution** — product count per category (doughnut)
- **Best Selling Products** — top 5 products last 30 days (bar chart)
- **Inventory Status** — in-stock / low-stock / out-of-stock (pie chart)

---

### 4.4 `products` App

**Purpose:** Product catalog with auto-generated barcodes and QR codes.

#### Models

**`Category`**

| Field         | Type          | Notes                        |
|---------------|---------------|------------------------------|
| `name`        | CharField     | Unique                       |
| `slug`        | SlugField     | Auto-generated from name     |
| `image`       | ImageField    | Optional, `categories/`      |
| `description` | TextField     | Optional                     |
| `is_active`   | BooleanField  | Default: True                |

**`Brand`**

| Field         | Type          | Notes                        |
|---------------|---------------|------------------------------|
| `name`        | CharField     | Unique                       |
| `logo`        | ImageField    | Optional, `brands/`          |
| `description` | TextField     | Optional                     |
| `website`     | URLField      | Optional                     |
| `is_active`   | BooleanField  | Default: True                |

**`Product`**

| Field                 | Type          | Notes                                   |
|-----------------------|---------------|-----------------------------------------|
| `name`                | CharField     | Max 200 chars                           |
| `product_code`        | CharField     | Auto-generated `FIM-XXXXXXXX`           |
| `barcode_number`      | CharField     | Defaults to product_code                |
| `barcode_image`       | ImageField    | Auto-generated Code128 barcode PNG      |
| `qr_code`             | ImageField    | Auto-generated QR code PNG              |
| `slug`                | SlugField     | Auto-generated                          |
| `category`            | FK->Category  | SET_NULL on delete                      |
| `brand`               | FK->Brand     | SET_NULL on delete, optional            |
| `supplier`            | FK->Supplier  | SET_NULL on delete, optional            |
| `purchase_price`      | DecimalField  | Cost price                              |
| `selling_price`       | DecimalField  | MRP / selling price                     |
| `gst_percentage`      | DecimalField  | Default 18%                             |
| `description`         | TextField     | Optional                                |
| `warranty`            | CharField     | Optional                                |
| `status`              | CharField     | `active`, `inactive`, `discontinued`    |
| `stock_quantity`      | IntegerField  | Current stock                           |
| `low_stock_threshold` | IntegerField  | Default 5                               |

**Properties:** `is_low_stock`, `is_out_of_stock`, `profit_margin`, `main_image`

**`ProductImage`**

| Field        | Type         | Notes                    |
|--------------|--------------|--------------------------|
| `product`    | FK->Product  | CASCADE                  |
| `image`      | ImageField   | `products/`              |
| `is_primary` | BooleanField | Primary display image    |

#### URLs

| URL                                 | View                  | Description              |
|-------------------------------------|-----------------------|--------------------------|
| `/products/`                        | `product_list`        | List all products        |
| `/products/add/`                    | `product_add`         | Add new product          |
| `/products/<pk>/`                   | `product_detail`      | Product detail           |
| `/products/<pk>/edit/`              | `product_edit`        | Edit product             |
| `/products/<pk>/delete/`            | `product_delete`      | Delete product           |
| `/products/<pk>/barcode/`           | `product_barcode`     | View barcode             |
| `/products/<pk>/qrcode/`            | `product_qrcode`      | View QR code             |
| `/products/search/`                 | `product_search_ajax` | AJAX product search (POS)|
| `/products/categories/`             | `category_list`       | List categories          |
| `/products/categories/add/`         | `category_add`        | Add category             |
| `/products/categories/<pk>/edit/`   | `category_edit`       | Edit category            |
| `/products/categories/<pk>/delete/` | `category_delete`     | Delete category          |
| `/products/brands/`                 | `brand_list`          | List brands              |
| `/products/brands/add/`             | `brand_add`           | Add brand                |
| `/products/brands/<pk>/edit/`       | `brand_edit`          | Edit brand               |
| `/products/brands/<pk>/delete/`     | `brand_delete`        | Delete brand             |

---

### 4.5 `inventory` App

**Purpose:** Real-time stock tracking — movements, adjustments, damaged goods.

#### Models

**`StockMovement`**

| Field             | Type           | Notes                                        |
|-------------------|----------------|----------------------------------------------|
| `product`         | FK->Product    | CASCADE                                      |
| `movement_type`   | CharField      | `in`, `out`, `adjust`, `damaged`, `return`   |
| `quantity`        | IntegerField   |                                              |
| `quantity_before` | IntegerField   | Snapshot before change                       |
| `quantity_after`  | IntegerField   | Snapshot after change                        |
| `reason`          | TextField      | Optional                                     |
| `reference`       | CharField      | Purchase/Sale order reference                |
| `created_by`      | FK->CustomUser | SET_NULL on delete                           |

**`StockAdjustment`**

| Field             | Type           | Notes                                   |
|-------------------|----------------|-----------------------------------------|
| `product`         | FK->Product    | CASCADE                                 |
| `adjustment_type` | CharField      | `add` or `reduce`                       |
| `quantity`        | IntegerField   |                                         |
| `reason`          | TextField      |                                         |
| `created_by`      | FK->CustomUser |                                         |

> NOTE: Saving a `StockAdjustment` automatically updates `Product.stock_quantity` and creates a `StockMovement` record.

#### URLs

| URL                        | View            | Description              |
|----------------------------|-----------------|--------------------------|
| `/inventory/`              | `stock_list`    | Stock overview           |
| `/inventory/low-stock/`    | `low_stock`     | Products below threshold |
| `/inventory/out-of-stock/` | `out_of_stock`  | Zero stock products      |
| `/inventory/stock-in/`     | `stock_in`      | Add stock manually       |
| `/inventory/stock-out/`    | `stock_out`     | Remove stock manually    |
| `/inventory/adjust/`       | `stock_adjust`  | Adjust stock             |
| `/inventory/history/`      | `stock_history` | All movement history     |
| `/inventory/damaged/`      | `damaged_stock` | Damaged goods log        |

---

### 4.6 `sales` App

**Purpose:** Point-of-Sale billing, invoice generation (PDF), and sales history.

#### Models

**`Sale`**

| Field                | Type           | Notes                                    |
|----------------------|----------------|------------------------------------------|
| `invoice_number`     | CharField      | Auto-generated `INV-YYYYMM-XXXXXX`       |
| `customer`           | FK->Customer   | Optional (walk-in sales)                 |
| `sale_date`          | DateTimeField  |                                          |
| `payment_method`     | CharField      | `cash`, `upi`, `card`                    |
| `status`             | CharField      | `completed`, `refunded`, `partial_refund`|
| `subtotal`           | DecimalField   |                                          |
| `discount_amount`    | DecimalField   |                                          |
| `discount_percentage`| DecimalField   |                                          |
| `gst_amount`         | DecimalField   |                                          |
| `grand_total`        | DecimalField   |                                          |
| `amount_paid`        | DecimalField   |                                          |
| `change_amount`      | DecimalField   | Change returned to customer              |
| `notes`              | TextField      | Optional                                 |
| `created_by`         | FK->CustomUser |                                          |

**`SaleItem`**

| Field            | Type           | Notes                   |
|------------------|----------------|-------------------------|
| `sale`           | FK->Sale       | CASCADE                 |
| `product`        | FK->Product    | CASCADE                 |
| `quantity`       | IntegerField   |                         |
| `unit_price`     | DecimalField   |                         |
| `discount`       | DecimalField   |                         |
| `gst_percentage` | DecimalField   |                         |
| `total_price`    | DecimalField   |                         |

#### URLs

| URL                         | View               | Description             |
|-----------------------------|--------------------|-------------------------|
| `/sales/`                   | `sale_list`        | All sales list          |
| `/sales/pos/`               | `pos`              | POS terminal            |
| `/sales/create/`            | `sale_create`      | Create sale (API)       |
| `/sales/<pk>/`              | `sale_detail`      | Sale detail             |
| `/sales/<pk>/invoice/`      | `sale_invoice`     | HTML invoice            |
| `/sales/<pk>/invoice/pdf/`  | `sale_invoice_pdf` | PDF invoice download    |
| `/sales/<pk>/edit/`         | `sale_edit`        | Edit sale               |
| `/sales/<pk>/delete/`       | `sale_delete`      | Delete sale             |

---

### 4.7 `purchase` App

**Purpose:** Manage purchase orders from suppliers, receive stock, track payments.

#### Models

**`PurchaseOrder`**

| Field               | Type           | Notes                                         |
|---------------------|----------------|-----------------------------------------------|
| `order_number`      | CharField      | Auto-generated `PO-XXXXXXXX`                  |
| `supplier`          | FK->Supplier   | CASCADE                                       |
| `order_date`        | DateField      | Auto-set                                      |
| `expected_delivery` | DateField      | Optional                                      |
| `status`            | CharField      | `pending`, `received`, `partial`, `cancelled` |
| `total_amount`      | DecimalField   |                                               |
| `paid_amount`       | DecimalField   |                                               |
| `notes`             | TextField      | Optional                                      |
| `created_by`        | FK->CustomUser |                                               |

**Property:** `balance_amount` = `total_amount - paid_amount`

**`PurchaseItem`**

| Field              | Type                | Notes      |
|--------------------|---------------------|------------|
| `purchase_order`   | FK->PurchaseOrder   | CASCADE    |
| `product`          | FK->Product         | CASCADE    |
| `quantity`         | IntegerField        |            |
| `purchase_price`   | DecimalField        |            |
| `received_quantity`| IntegerField        | Default 0  |

**`SupplierPayment`**

| Field            | Type                | Notes                                   |
|------------------|---------------------|-----------------------------------------|
| `purchase_order` | FK->PurchaseOrder   | CASCADE                                 |
| `amount`         | DecimalField        |                                         |
| `payment_method` | CharField           | `cash`, `upi`, `card`, `bank`, `cheque` |
| `payment_date`   | DateField           | Auto-set                                |
| `note`           | TextField           | Optional                                |
| `created_by`     | FK->CustomUser      |                                         |

#### URLs

| URL                           | View               | Description             |
|-------------------------------|--------------------|-------------------------|
| `/purchase/`                  | `purchase_list`    | All purchase orders     |
| `/purchase/add/`              | `purchase_add`     | Create purchase order   |
| `/purchase/<pk>/`             | `purchase_detail`  | PO detail               |
| `/purchase/<pk>/edit/`        | `purchase_edit`    | Edit PO                 |
| `/purchase/<pk>/receive/`     | `receive_stock`    | Mark stock as received  |
| `/purchase/<pk>/payment/`     | `add_payment`      | Record supplier payment |
| `/purchase/<pk>/invoice/`     | `purchase_invoice` | PO invoice              |
| `/purchase/<pk>/delete/`      | `purchase_delete`  | Delete PO               |

---

### 4.8 `customers` App

**Purpose:** Customer contact management with purchase history and reward points.

#### Model — `Customer`

| Field           | Type          | Notes               |
|-----------------|---------------|---------------------|
| `name`          | CharField     |                     |
| `phone`         | CharField     | Unique              |
| `email`         | EmailField    | Optional            |
| `address`       | TextField     | Optional            |
| `reward_points` | IntegerField  | Default 0           |
| `is_active`     | BooleanField  | Default True        |

**Properties:** `total_purchases` (sum of grand_total), `total_orders` (count)

#### URLs

| URL                       | View              | Description      |
|---------------------------|-------------------|------------------|
| `/customers/`             | `customer_list`   | All customers    |
| `/customers/add/`         | `customer_add`    | Add customer     |
| `/customers/<pk>/`        | `customer_detail` | Customer detail  |
| `/customers/<pk>/edit/`   | `customer_edit`   | Edit customer    |
| `/customers/<pk>/delete/` | `customer_delete` | Delete customer  |

---

### 4.9 `suppliers` App

**Purpose:** Supplier management with GST numbers and purchase order history.

#### Model — `Supplier`

| Field            | Type          | Notes         |
|------------------|---------------|---------------|
| `company_name`   | CharField     |               |
| `contact_person` | CharField     |               |
| `phone`          | CharField     |               |
| `email`          | EmailField    | Optional      |
| `address`        | TextField     | Optional      |
| `gst_number`     | CharField     | Optional      |
| `is_active`      | BooleanField  | Default True  |

**Property:** `total_purchases` (sum of all PO amounts)

#### URLs

| URL                       | View              | Description      |
|---------------------------|-------------------|------------------|
| `/suppliers/`             | `supplier_list`   | All suppliers    |
| `/suppliers/add/`         | `supplier_add`    | Add supplier     |
| `/suppliers/<pk>/`        | `supplier_detail` | Supplier detail  |
| `/suppliers/<pk>/edit/`   | `supplier_edit`   | Edit supplier    |
| `/suppliers/<pk>/delete/` | `supplier_delete` | Delete supplier  |

---

### 4.10 `employees` App

**Purpose:** HR management — employee profiles, attendance tracking, and leave management.

#### Models

**`Employee`**

| Field             | Type            | Notes                                         |
|-------------------|-----------------|-----------------------------------------------|
| `user`            | O2O->CustomUser | Optional link to login account                |
| `employee_id`     | CharField       | Auto-generated `EMP-XXXXXX`                   |
| `first_name`      | CharField       |                                               |
| `last_name`       | CharField       |                                               |
| `email`           | EmailField      | Optional                                      |
| `phone`           | CharField       |                                               |
| `designation`     | CharField       |                                               |
| `department`      | CharField       | Optional                                      |
| `salary`          | DecimalField    |                                               |
| `join_date`       | DateField       |                                               |
| `status`          | CharField       | `active`, `inactive`, `on_leave`, `terminated`|
| `profile_picture` | ImageField      | `employees/`                                  |

**`Attendance`**

| Field      | Type         | Notes                                           |
|------------|--------------|-------------------------------------------------|
| `employee` | FK->Employee | CASCADE                                         |
| `date`     | DateField    |                                                 |
| `status`   | CharField    | `present`, `absent`, `late`, `half_day`, `leave`|
| `check_in` | TimeField    | Optional                                        |
| `check_out`| TimeField    | Optional                                        |
| `notes`    | TextField    | Optional                                        |

> Unique together: `(employee, date)`

**`Leave`**

| Field        | Type           | Notes                                 |
|--------------|----------------|---------------------------------------|
| `employee`   | FK->Employee   | CASCADE                               |
| `leave_type` | CharField      | `sick`, `casual`, `annual`, `other`   |
| `start_date` | DateField      |                                       |
| `end_date`   | DateField      |                                       |
| `reason`     | TextField      |                                       |
| `status`     | CharField      | `pending`, `approved`, `rejected`     |
| `approved_by`| FK->CustomUser | SET_NULL on delete                    |

**Property:** `total_days`

#### URLs

| URL                                | View              | Description            |
|------------------------------------|-------------------|------------------------|
| `/employees/`                      | `employee_list`   | All employees          |
| `/employees/add/`                  | `employee_add`    | Add employee           |
| `/employees/<pk>/`                 | `employee_detail` | Employee detail        |
| `/employees/<pk>/edit/`            | `employee_edit`   | Edit employee          |
| `/employees/<pk>/delete/`          | `employee_delete` | Delete employee        |
| `/employees/attendance/`           | `attendance_list` | Attendance records     |
| `/employees/attendance/save/`      | `attendance_add`  | Mark attendance        |
| `/employees/leaves/`               | `leave_list`      | All leave requests     |
| `/employees/leaves/apply/`         | `leave_add`       | Apply for leave        |
| `/employees/leaves/<pk>/approve/`  | `leave_approve`   | Approve/reject leave   |

---

### 4.11 `reports` App

**Purpose:** Generate detailed reports with PDF and CSV export options.

#### URLs

| URL                        | View                  | Description                    |
|----------------------------|-----------------------|--------------------------------|
| `/reports/`                | `report_home`         | Reports home page              |
| `/reports/sales/`          | `sales_report`        | Sales report                   |
| `/reports/sales/pdf/`      | `sales_report_pdf`    | Sales report — PDF download    |
| `/reports/sales/csv/`      | `sales_report_csv`    | Sales report — CSV download    |
| `/reports/purchase/`       | `purchase_report`     | Purchase report                |
| `/reports/purchase/pdf/`   | `purchase_report_pdf` | Purchase report — PDF          |
| `/reports/profit/`         | `profit_report`       | Profit & loss report           |
| `/reports/inventory/`      | `inventory_report`    | Inventory valuation report     |
| `/reports/inventory/pdf/`  | `inventory_report_pdf`| Inventory report — PDF         |
| `/reports/customers/`      | `customer_report`     | Customer purchase report       |
| `/reports/suppliers/`      | `supplier_report`     | Supplier purchase report       |
| `/reports/employees/`      | `employee_report`     | Employee report                |

---

### 4.12 `notifications` App

**Purpose:** In-app notification system for stock alerts, sales, and system events.

#### Model — `Notification`

| Field               | Type           | Notes                                              |
|---------------------|----------------|----------------------------------------------------|
| `title`             | CharField      |                                                    |
| `message`           | TextField      |                                                    |
| `notification_type` | CharField      | `low_stock`, `sale`, `purchase`, `employee`, `system` |
| `is_read`           | BooleanField   | Default False                                      |
| `link`              | CharField      | Optional URL to link to                            |
| `user`              | FK->CustomUser | Optional — user-specific notification              |

---

### 4.13 `settings_app`

**Purpose:** Singleton model for company-wide settings applied globally.

#### Model — `CompanySettings`

| Field                | Type          | Notes                              |
|----------------------|---------------|------------------------------------|
| `company_name`       | CharField     | Default: `Fenix IT Mall`           |
| `company_logo`       | ImageField    | `settings/`                        |
| `tagline`            | CharField     |                                    |
| `phone`              | CharField     | Optional                           |
| `email`              | EmailField    | Optional                           |
| `address`            | TextField     | Optional                           |
| `gst_number`         | CharField     | Optional                           |
| `invoice_prefix`     | CharField     | Default: `INV`                     |
| `currency_symbol`    | CharField     | Default: Indian Rupee symbol       |
| `currency_code`      | CharField     | Default: `INR`                     |
| `low_stock_threshold`| IntegerField  | Default: 5                         |
| `theme`              | CharField     | `dark` or `light`                  |
| `website`            | URLField      | Optional                           |

> Singleton pattern: `pk` is always forced to `1`; use `CompanySettings.get_settings()`.

---

## 5. Database Models (ERD)

```
CustomUser (accounts)
    |
    |--< Employee (employees) [OneToOne]
    |       |--< Attendance
    |       `--< Leave
    |
    `--< Notification (notifications)

Category (products) --< Product (products) >-- Brand
                             |
                             |--< ProductImage
                             |--< StockMovement (inventory)
                             |--< StockAdjustment (inventory)
                             |--< SaleItem (sales) >--- Sale --> Customer
                             `--< PurchaseItem (purchase) >-- PurchaseOrder --> Supplier
                                                                     `--< SupplierPayment

CompanySettings (settings_app) [Singleton, pk=1]
```

---

## 6. URL Route Map

```
/                     --> Redirects to /accounts/login/
/admin/               --> Django admin panel
/accounts/            --> Authentication & user management
/dashboard/           --> Main dashboard
/products/            --> Product catalog + categories + brands
/inventory/           --> Stock management
/sales/               --> POS + invoices
/purchase/            --> Purchase orders
/customers/           --> Customer CRM
/suppliers/           --> Supplier management
/employees/           --> HR: employees + attendance + leaves
/reports/             --> Reports & analytics
/notifications/       --> Notification management
/settings/            --> Company settings
```

---

## 7. Static Assets

### CSS Files (`static/css/`)

| File             | Purpose                              |
|------------------|--------------------------------------|
| `main.css`       | Primary stylesheet — all components  |
| `variables.css`  | CSS custom properties (design tokens)|
| `layout.css`     | Sidebar, navbar, page layout         |
| `dashboard.css`  | Dashboard-specific card & chart CSS  |
| `forms.css`      | Form inputs, labels, validation      |
| `buttons.css`    | Button variants and states           |
| `tables.css`     | Data table styles                    |
| `glass.css`      | Glassmorphism card effects           |
| `animations.css` | CSS keyframe animations              |
| `darkmode.css`   | Dark mode variable overrides         |
| `responsive.css` | Breakpoint media queries             |

### JavaScript Files (`static/js/`)

| File            | Purpose                                         |
|-----------------|-------------------------------------------------|
| `main.js`       | Global utilities, toast notifications           |
| `dashboard.js`  | Chart.js initialization (6 charts)              |
| `pos.js`        | POS terminal: product search, cart, billing     |
| `sidebar.js`    | Sidebar open/close & active link tracking       |
| `modal.js`      | Reusable modal open/close utilities             |
| `theme.js`      | Dark to Light theme toggle with localStorage    |
| `three_hero.js` | Three.js 3D animated background for login page  |

---

## 8. Templates Structure

```
templates/
|-- base.html                   # Master template: sidebar, navbar, toast
|-- accounts/
|   |-- login.html
|   |-- register.html
|   |-- profile.html
|   |-- password_change.html
|   |-- user_list.html
|   |-- user_form.html
|   `-- admin_change_password.html
|-- dashboard/
|   |-- index.html
|   `-- recent_activity.html
|-- products/
|   |-- list.html, detail.html, form.html
|   |-- category_list.html, category_form.html
|   `-- brand_list.html, brand_form.html
|-- inventory/
|   |-- list.html, history.html
|   |-- low_stock.html, out_of_stock.html
|   `-- adjust.html, damaged.html
|-- sales/
|   |-- list.html, detail.html
|   |-- pos.html
|   `-- invoice.html
|-- purchase/
|   |-- list.html, detail.html, form.html
|   `-- invoice.html
|-- customers/
|   `-- list.html, detail.html, form.html
|-- suppliers/
|   `-- list.html, detail.html, form.html
|-- employees/
|   |-- list.html, detail.html, form.html
|   |-- attendance.html
|   `-- leaves.html
|-- reports/
|   |-- home.html
|   |-- sales.html, purchase.html, profit.html
|   `-- inventory.html, customers.html, suppliers.html, employees.html
|-- notifications/
|   `-- list.html
`-- settings_app/
    `-- settings.html
```

---

## 9. Configuration & Settings

### Key Settings (`fenix_it_mall/settings.py`)

| Setting                       | Value                             |
|-------------------------------|-----------------------------------|
| `DEBUG`                       | `True` (change for production)    |
| `ALLOWED_HOSTS`               | `['*']`                           |
| `AUTH_USER_MODEL`             | `accounts.CustomUser`             |
| `TIME_ZONE`                   | `Asia/Kolkata`                    |
| `LANGUAGE_CODE`               | `en-us`                           |
| `LOGIN_URL`                   | `/accounts/login/`                |
| `LOGIN_REDIRECT_URL`          | `/dashboard/`                     |
| `LOGOUT_REDIRECT_URL`         | `/accounts/login/`                |
| `STATIC_URL`                  | `/static/`                        |
| `MEDIA_URL`                   | `/media/`                         |
| `DATA_UPLOAD_MAX_MEMORY_SIZE` | `10 MB`                           |

### Installed Apps Order
```
django.contrib.admin, django.contrib.auth, django.contrib.contenttypes,
django.contrib.sessions, django.contrib.messages, django.contrib.staticfiles,
core, accounts, dashboard, products, inventory, sales, purchase,
customers, suppliers, employees, reports, notifications, settings_app
```

---

## 10. Running the Project

### Prerequisites
- Python 3.10+
- pip

### Setup Steps

```bash
# 1. Navigate to project directory
cd finix_it_mall_demo_426

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Load sample fixtures (if available)
python manage.py loaddata fixtures/

# 7. Run development server
python manage.py runserver
```

### Access Points

| URL                               | Description              |
|-----------------------------------|--------------------------|
| `http://127.0.0.1:8000/`          | Redirects to login       |
| `http://127.0.0.1:8000/admin/`    | Django admin panel       |
| `http://127.0.0.1:8000/dashboard/`| Main application         |

---

## 11. Role-Based Access Control

| Role         | Access Level                                                    |
|--------------|-----------------------------------------------------------------|
| **Admin**    | Full access — users, settings, all CRUD, reports                |
| **Manager**  | Most features except user management and system settings        |
| **Cashier**  | POS billing, view products, view inventory (read-only reports)  |
| **Employee** | Limited view access                                             |

### Permission Properties

```python
user.is_admin    # True for admin or superuser
user.is_manager  # True for admin or manager
user.is_cashier  # True for admin, manager, or cashier
```

Access is enforced in views with checks like:

```python
if not request.user.is_admin:
    messages.error(request, 'Permission denied.')
    return redirect('dashboard:index')
```

---

## Appendix — Auto-Generated IDs

| Entity        | Format                  | Example             |
|---------------|-------------------------|---------------------|
| Product Code  | `FIM-XXXXXXXX`          | `FIM-A1B2C3D4`      |
| Invoice No.   | `INV-YYYYMM-XXXXXX`     | `INV-202608-AB12CD` |
| Purchase Order| `PO-XXXXXXXX`           | `PO-1A2B3C4D`       |
| Employee ID   | `EMP-XXXXXX`            | `EMP-F3G7H1`        |

---

*Documentation generated on 2026-08-14 | Fenix IT Mall — BCA Project*
