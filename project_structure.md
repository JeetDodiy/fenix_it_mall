# Fenix IT Mall – Complete Project Structure

This document provides a comprehensive overview of the **Fenix IT Mall** Django project, including all apps, templates, static assets, recent feature additions, and architectural patterns.

---

## 📁 High-Level Directory Structure

```text
fenix_it_mall_demo_426/
│
├── fenix_it_mall/          # Django project configuration
│   ├── settings.py         # All project settings (DB, apps, middleware, static/media)
│   ├── urls.py             # Main URL router (includes all app URLs)
│   ├── wsgi.py             # WSGI entry point for production
│   └── asgi.py             # ASGI entry point for async support
│
├── manage.py               # Django CLI management script
├── db.sqlite3              # SQLite database (development)
├── requirements.txt        # Python package dependencies
├── implementation_plan.md  # Detailed roadmap and implementation checklist
├── task.md                 # Project progress tracker
├── project_structure.md    # This file
├── ui.md                   # UI/UX design system documentation
│
├── accounts/               # User authentication & authorization
├── core/                   # Base app (landing page, context processors, utilities)
├── dashboard/              # Main dashboard with analytics and charts
├── products/               # Product catalog (categories, brands, products)
├── inventory/              # Stock tracking (movements, adjustments, low stock alerts)
├── sales/                  # Point of Sale (POS) and invoice management
├── purchase/               # Purchase orders and supplier payments
├── customers/              # Customer directory and loyalty management
├── suppliers/              # Supplier directory and tracking
├── employees/              # HR module (staff, attendance, leave requests)
├── reports/                # Analytics reports (sales, purchases, profit/loss, exports)
├── notifications/          # System-wide alerts and toast messages
├── settings_app/           # Global company settings (name, logo, tax config)
│
├── templates/              # Django HTML templates (organized by app)
├── static/                 # CSS, JavaScript, and frontend assets
├── media/                  # User-uploaded files (product images, logos, profiles)
├── fixtures/               # Sample data for testing and demo
└── venv/                   # Python virtual environment (not in version control)
```

---

## 🧩 Django Apps & Responsibilities

| App | Purpose | Key Models | Key Features |
|-----|---------|------------|--------------|
| **`accounts`** | User authentication, roles (Admin, Manager, Cashier, Employee), profile management | `CustomUser` | Role-based permissions, password change by admin, profile editing |
| **`core`** | Base layout, landing page, error pages, global context processors | *(None)* | Provides `base.html`, injects company settings and notifications globally |
| **`dashboard`** | Main analytics dashboard with charts and business intelligence | *(None)* | Charts.js visualizations, GSAP animations, summary cards |
| **`products`** | Product catalog with categories, brands, barcodes, QR codes | `Category`, `Brand`, `Product`, `ProductImage` | Auto-generate barcodes/QR codes, multi-image support, stock tracking |
| **`inventory`** | Stock movements (in/out/adjust/damage), low stock alerts | `StockMovement`, `StockAdjustment` | Real-time stock updates, history tracking, damaged goods log |
| **`sales`** | Point of Sale (POS), invoice generation, sale history, **invoice editing** | `Sale`, `SaleItem` | Alpine.js POS, barcode scanner support, PDF invoices, **full invoice edit capability** |
| **`purchase`** | Purchase orders from suppliers, receiving stock, supplier payments | `PurchaseOrder`, `PurchaseItem`, `SupplierPayment` | Multi-item POs, stock auto-update on receive, payment tracking |
| **`customers`** | Customer directory, purchase history, loyalty points | `Customer` | Customer profiles, transaction history, reward points system |
| **`suppliers`** | Supplier directory, purchase tracking | `Supplier` | Supplier profiles, purchase history, contact management |
| **`employees`** | HR module for staff management, attendance, leave requests | `Employee`, `Attendance`, `Leave` | Daily attendance tracking, leave approval workflow |
| **`reports`** | Generate downloadable reports (PDF/CSV), analytics | *(None)* | Sales, purchases, inventory, profit/loss, customer/supplier reports |
| **`notifications`** | System alerts, low stock warnings, toast messages | `Notification` | Real-time alerts, read/unread status, auto-dismiss toasts |
| **`settings_app`** | Global company configuration (name, logo, tax rates, themes) | `CompanySettings` | Single-instance settings, logo upload, tax configuration |

---

## 📄 Complete Template Structure

All templates extend `base.html` which provides:
- Responsive sidebar navigation
- Top navbar with theme toggle, notifications, and user dropdown
- Toast message system
- Alpine.js integration for interactivity

### **`templates/` Directory**

```text
templates/
│
├── base.html                      # Master layout (sidebar, navbar, footer, theme toggle)
│
├── accounts/                      # User authentication & management
│   ├── login.html                 # Login page (with company logo support)
│   ├── register.html              # User registration
│   ├── profile.html               # User profile editing
│   ├── password_change.html       # User password change
│   ├── admin_change_password.html # Admin change user password
│   ├── user_list.html             # User management list (admin only)
│   └── user_form.html             # Add/edit user form
│
├── core/                          # Landing and error pages
│   ├── 403.html                   # Forbidden error page
│   ├── 404.html                   # Not found error page
│   └── 500.html                   # Server error page
│
├── dashboard/                     # Analytics dashboard
│   └── index.html                 # Main dashboard (charts, stats, GSAP animations)
│
├── products/                      # Product catalog management
│   ├── list.html                  # Product list with search/filter
│   ├── detail.html                # Product detail page
│   ├── form.html                  # Add/edit product form
│   ├── category_list.html         # Category list
│   ├── category_form.html         # Add/edit category
│   ├── brand_list.html            # Brand list
│   ├── brand_form.html            # Add/edit brand
│   ├── barcode.html               # View/print barcode
│   └── qrcode.html                # View/print QR code
│
├── inventory/                     # Stock management
│   ├── list.html                  # Inventory overview
│   ├── history.html               # Stock movement history
│   ├── stock_in.html              # Add stock
│   ├── stock_out.html             # Remove stock
│   ├── adjust.html                # Adjust stock levels
│   ├── damaged.html               # Log damaged goods
│   ├── low_stock.html             # Low stock alert list
│   └── out_of_stock.html          # Out of stock items
│
├── sales/                         # Sales & invoicing
│   ├── pos.html                   # Point of Sale interface (Alpine.js, barcode scanner)
│   ├── list.html                  # Sales history with filters
│   ├── detail.html                # Invoice detail view
│   ├── edit.html                  # **Invoice edit page (NEW)** – modify items, qty, price, customer, payment
│   ├── invoice.html               # Printable invoice template
│   └── delete_confirm.html        # Delete sale confirmation
│
├── purchase/                      # Purchase order management
│   ├── list.html                  # Purchase order list
│   ├── detail.html                # PO detail view
│   ├── form.html                  # Add/edit purchase order
│   ├── invoice.html               # Purchase invoice
│   ├── payment_form.html          # Supplier payment form
│   ├── receive_confirm.html       # Receive stock confirmation
│   └── delete_confirm.html        # Delete PO confirmation
│
├── customers/                     # Customer management
│   ├── list.html                  # Customer directory
│   ├── detail.html                # Customer profile & purchase history
│   ├── form.html                  # Add/edit customer
│   └── delete_confirm.html        # Delete customer confirmation
│
├── suppliers/                     # Supplier management
│   ├── list.html                  # Supplier directory
│   ├── detail.html                # Supplier profile & purchase history
│   ├── form.html                  # Add/edit supplier
│   └── delete_confirm.html        # Delete supplier confirmation
│
├── employees/                     # HR management
│   ├── list.html                  # Employee list
│   ├── detail.html                # Employee profile
│   ├── form.html                  # Add/edit employee
│   ├── attendance.html            # Attendance tracking
│   ├── leaves.html                # Leave request list
│   ├── leave_form.html            # Submit leave request
│   └── delete_confirm.html        # Delete employee confirmation
│
├── reports/                       # Analytics & exports
│   ├── home.html                  # Reports hub
│   ├── sales.html                 # Sales report (filterable, exportable)
│   ├── purchase.html              # Purchase report
│   ├── inventory.html             # Inventory report
│   ├── profit.html                # Profit/loss report
│   ├── customers.html             # Customer analytics
│   ├── suppliers.html             # Supplier analytics
│   └── employees.html             # Employee report
│
├── notifications/                 # System alerts
│   └── list.html                  # Notification center
│
├── settings_app/                  # Global settings
│   └── settings.html              # Company settings form
│
└── includes/                      # Reusable template components
    ├── alerts.html                # Toast message component
    ├── breadcrumbs.html           # Breadcrumb navigation
    ├── footer.html                # Page footer
    ├── loader.html                # Loading spinner
    ├── modal.html                 # Modal dialog
    ├── navbar.html                # Top navigation bar
    ├── pagination.html            # Pagination controls
    ├── searchbar.html             # Search bar component
    ├── sidebar.html               # Sidebar navigation
    └── theme_switch.html          # Dark/light theme toggle
```

---

## 🎨 Static Assets Structure

### **CSS Files** (`static/css/`)

| File | Purpose |
|------|---------|
| **`main.css`** | Master stylesheet that imports all others |
| **`variables.css`** | CSS custom properties (colors, spacing, shadows, transitions) |
| **`layout.css`** | Grid layouts, sidebar, navbar, main content area |
| **`glass.css`** | Glassmorphism effects (backdrop-blur, transparency) |
| **`forms.css`** | Form inputs, selects, textareas, validation styles |
| **`buttons.css`** | Button variants (primary, outline, danger, warning, etc.) |
| **`tables.css`** | Table styles, responsive tables, striped rows |
| **`dashboard.css`** | Dashboard-specific cards, charts, stat counters |
| **`animations.css`** | CSS transitions, hover effects, keyframe animations |
| **`darkmode.css`** | Dark theme overrides (toggled via `.light-theme` class on `<html>`) |
| **`responsive.css`** | Mobile breakpoints, responsive adjustments |

### **JavaScript Files** (`static/js/`)

| File | Purpose |
|------|---------|
| **`main.js`** | Global utilities (theme toggle, toast auto-dismiss, dropdown helpers) |
| **`dashboard.js`** | Chart.js initialization, GSAP counter animations |
| **`pos.js`** | Alpine.js POS logic (cart management, barcode scanner, payment methods) |
| **`sidebar.js`** | Sidebar collapse/expand, mobile menu toggle |
| **`theme.js`** | Dark/light theme switcher with localStorage persistence |
| **`modal.js`** | Modal dialog open/close logic |
| **`three_hero.js`** | Three.js 3D animations for landing page hero section |

---

## 📦 Media Upload Structure

```text
media/
├── products/          # Product photos (uploaded by admin)
├── barcodes/          # Auto-generated product barcodes (PNG)
├── qrcodes/           # Auto-generated product QR codes (PNG)
├── brands/            # Brand logos
├── categories/        # Category images
├── profiles/          # User profile pictures
└── settings/          # Company logo
```

---

## 🆕 Recent Feature Additions

### **1. Splash Screen on Page Load**
- **Location**: `templates/base.html`
- **Description**: Beautiful animated splash screen displays when loading any page
  - Shows company logo (if uploaded) or default ⚡ icon
  - Company name and tagline
  - Loading spinner animation
  - Auto-hides after 800ms
  - Smooth fade-out transition
- **Styling**: Gradient background, pulsing logo, rotating loader

### **2. Company Logo in Sidebar**
- **Location**: `templates/base.html` → sidebar-brand section
- **Description**: Company logo now appears in the top-left corner of the sidebar
  - Displays uploaded logo from company settings
  - Falls back to ⚡ icon if no logo is set
  - Responsive sizing (48x48px)
  - Glow effect with box-shadow
- **Context**: Uses `company_settings` from global context processor

### **3. Direct Login on Root URL**
- **Change**: Root URL (`/`) now redirects directly to the login page instead of showing a landing page
- **Reason**: Faster access for daily users, removes unnecessary landing step
- **Location**: `fenix_it_mall/urls.py` → `RedirectView` to `/accounts/login/`

### **4. Company Logo on Login Page**
- **Location**: `templates/accounts/login.html`
- **Description**: Login page now displays the company logo (if uploaded in settings) above the login form
- **Fallback**: Shows default ⚡ icon if no logo is set
- **Context**: Uses `company_settings` from global context processor

### **3. Admin Password Change for Users**
- **Location**: `accounts/views.py`, `templates/accounts/admin_change_password.html`
- **Description**: Admins can now change any user's password without knowing their current password
- **Access**: Admin-only (role-based permission check)
- **UI**: 🔑 button added to user list and user edit pages

### **4. Invoice Edit Functionality**
- **Location**: `sales/views.py` → `sale_edit()`, `templates/sales/edit.html`
- **Description**: Full invoice editing after sale completion:
  - Add/remove/change items on invoice
  - Update product, quantity, unit price per line
  - Change customer, payment method, status
  - Modify discount percentage
  - Live total recalculation with Alpine.js
  - Automatic stock adjustment (restores old stock, deducts new stock)
- **Access**: Manager and Admin roles
- **UI**: ✏️ Edit button added to:
  - Sale detail page header
  - Sales history table (Actions column)
- **Stock Safety**: Transaction-wrapped to prevent stock inconsistencies

---

## 🛠 Frontend Technology Stack

| Technology | Usage |
|------------|-------|
| **Alpine.js** | Reactive components (POS cart, invoice edit, dropdowns, modals) |
| **Chart.js** | Dashboard analytics charts (line, bar, doughnut) |
| **GSAP** | Animation library (dashboard counter animations, smooth transitions) |
| **Three.js** | 3D animations on landing page hero section |
| **Custom CSS** | Glassmorphism aesthetic, dark mode, responsive design |
| **CSS Variables** | Theme system with light/dark mode toggle |

---

## 🗄 Database Architecture

### **Current Setup**
- **Database**: SQLite (`db.sqlite3`)
- **ORM**: Django ORM (database-agnostic for easy migration to PostgreSQL/MySQL)

### **Key Model Relationships**

```text
CustomUser (accounts)
    ├─→ Sale.created_by (many sales created by one user)
    ├─→ StockMovement.created_by
    └─→ PurchaseOrder.created_by

Customer (customers)
    └─→ Sale.customer (one customer has many sales)

Product (products)
    ├─→ SaleItem.product (one product appears in many sales)
    ├─→ PurchaseItem.product (one product in many purchase orders)
    ├─→ StockMovement.product (one product has many stock movements)
    ├─→ Category.products (one category has many products)
    └─→ Brand.products (one brand has many products)

Sale (sales)
    └─→ SaleItem (one sale has many items)

PurchaseOrder (purchase)
    └─→ PurchaseItem (one PO has many items)

Supplier (suppliers)
    └─→ PurchaseOrder.supplier (one supplier has many POs)

Employee (employees)
    ├─→ Attendance (one employee has many attendance records)
    └─→ Leave (one employee has many leave requests)
```

---

## 🎯 Design Patterns & Conventions

### **URL Naming Convention**
- `app_name:list` – List view (e.g., `sales:list`, `products:list`)
- `app_name:detail` – Detail view with `pk` (e.g., `sales:detail`)
- `app_name:create` or `app_name:add` – Create new record
- `app_name:edit` – Edit existing record
- `app_name:delete` – Delete confirmation

### **Template Inheritance**
```
base.html (master layout)
    └─→ app/list.html (list pages)
    └─→ app/detail.html (detail pages)
    └─→ app/form.html (create/edit forms)
```

### **Form Styling**
All forms use consistent classes:
- `.form-input` – Text inputs, numbers, emails
- `.form-select` – Dropdowns
- `.form-textarea` – Textareas
- `.form-label` – Labels
- `.form-error` – Validation errors
- `.form-hint` – Help text

### **Button Styles**
- `.btn-primary` – Main actions (save, submit, create)
- `.btn-danger` – Destructive actions (delete)
- `.btn-warning` – Warning actions (edit, change)
- `.btn-outline` – Secondary actions (cancel, back)
- `.btn-sm` – Small buttons for table actions

### **Permission Guards**
- `@login_required` – All views require authentication
- `request.user.is_admin` – Admin-only actions
- `request.user.is_manager` – Manager+ actions
- `request.user.is_cashier` – Cashier+ actions (POS)

---

## 📊 App-Specific Details

### **Sales App Deep Dive**

**Views:**
- `pos()` – Point of Sale interface (POST creates sale + stock deduction)
- `sale_list()` – Sales history with filters (date range, payment method, search)
- `sale_detail()` – View invoice details
- `sale_edit()` – **[NEW]** Edit completed invoice (manager+ only)
- `sale_invoice()` – Printable HTML invoice
- `sale_invoice_pdf()` – Generate PDF using ReportLab
- `sale_delete()` – Delete sale (admin only)

**URLs:**
```python
/sales/                      → sale_list      (sales:list)
/sales/pos/                  → pos            (sales:pos)
/sales/<pk>/                 → sale_detail    (sales:detail)
/sales/<pk>/edit/            → sale_edit      (sales:edit) [NEW]
/sales/<pk>/invoice/         → sale_invoice   (sales:invoice)
/sales/<pk>/invoice/pdf/     → invoice_pdf    (sales:invoice_pdf)
/sales/<pk>/delete/          → sale_delete    (sales:delete)
```

**Key Features:**
- Barcode scanner integration in POS
- Keyboard shortcuts (F12 = submit, Alt+C = clear cart, 1/2/3 = payment methods)
- Real-time cart calculation with Alpine.js
- GST (18%) auto-calculated
- Change calculation for cash payments
- Multi-payment method support (Cash, UPI, Card)
- **Full edit capability after sale completion** (items, quantities, prices, discount, customer)

---

## 🚀 Future Enhancements

- [ ] Multi-warehouse support
- [ ] Advanced reporting with date range exports
- [ ] SMS/email notifications for low stock
- [ ] Barcode label printing from product page
- [ ] Customer loyalty program points redemption
- [ ] Employee commission tracking
- [ ] Purchase order approval workflow
- [ ] Integration with payment gateways
- [ ] REST API for mobile POS app
- [ ] Advanced analytics dashboard with filters

---

## 📝 Notes

- **Entry Point**: Root URL (`/`) redirects directly to `/accounts/login/` for faster access
- **Company Branding**: Login page displays company logo from settings (with ⚡ icon fallback)
- **Theme System**: Toggle between light/dark themes with localStorage persistence
- **Toast Messages**: Auto-dismiss after 3.5 seconds with staggered animations
- **Responsive Design**: Mobile-first approach, works on tablets and phones
- **Security**: Role-based access control enforced in views and templates
- **Stock Safety**: All stock operations are transaction-wrapped to prevent race conditions
- **PDF Generation**: ReportLab used for invoice PDFs (install with `pip install reportlab`)

---

**Last Updated**: August 14, 2026  
**Project Version**: 1.0  
**Django Version**: 4.2+  
**Python Version**: 3.10+
