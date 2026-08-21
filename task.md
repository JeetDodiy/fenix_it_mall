# Fenix IT Mall – Task List

## Phase 1 – Project Setup & Core
- [/] Install Python packages (django, pillow, reportlab, python-barcode, qrcode)
- [ ] Create Django project `fenix_it_mall`
- [ ] Create all 13 Django apps
- [ ] Configure `settings.py`
- [ ] Create `requirements.txt`
- [ ] Build base template (`core/base.html`)
- [ ] Build landing page (`core/landing.html`) with Three.js hero
- [ ] Build 404/403/500 pages
- [ ] Core context processors
- [ ] Static file structure (css/js/images)
- [ ] Configure `core/urls.py` and main `urls.py`

## Phase 2 – Accounts & Authentication
- [ ] CustomUser model with roles
- [ ] Login, Logout, Register views
- [ ] Forgot Password / Change Password
- [ ] Profile view + Edit Profile
- [ ] Role-based permission decorators
- [ ] Auth templates (glassmorphism style)

## Phase 3 – Dashboard
- [ ] Dashboard views with aggregated stats
- [ ] Chart.js JSON API endpoints
- [ ] Dashboard template with stat cards
- [ ] Recent activities section
- [ ] Quick actions panel
- [ ] GSAP counter animations

## Phase 4 – Products, Categories, Brands
- [ ] Category model + CRUD
- [ ] Brand model + CRUD
- [ ] Product model (full fields) + CRUD
- [ ] ProductImage model (multiple images)
- [ ] Barcode generation
- [ ] QR Code generation
- [ ] Product list with search/filter/pagination
- [ ] Product detail view

## Phase 5 – Inventory
- [ ] StockMovement model
- [ ] Current stock view
- [ ] Low stock / Out of stock views
- [ ] Stock in / Stock out forms
- [ ] Stock adjustment
- [ ] Stock history

## Phase 6 – Suppliers & Purchase
- [ ] Supplier model + CRUD
- [ ] PurchaseOrder model + CRUD
- [ ] PurchaseItem model
- [ ] SupplierPayment model
- [ ] Receive stock flow
- [ ] Purchase invoice template

## Phase 7 – Customers & Sales & POS
- [ ] Customer model + CRUD
- [ ] Sale model + SaleItem model
- [ ] Sales invoice view + PDF (ReportLab)
- [ ] POS system with barcode scan
- [ ] Alpine.js cart
- [ ] Payment modal (Cash/UPI/Card)
- [ ] Invoice print view

## Phase 8 – Employees
- [ ] Employee model + CRUD
- [ ] Attendance model + views
- [ ] Leave model + views
- [ ] Salary model

## Phase 9 – Reports
- [ ] Sales report with date filter
- [ ] Purchase report
- [ ] Profit/Loss report
- [ ] Inventory report
- [ ] PDF export (ReportLab)
- [ ] CSV export

## Phase 10 – Notifications & Settings
- [ ] Notification model + context processor
- [ ] Toast notification JS
- [ ] CompanySettings singleton model
- [ ] Settings view (company info, logo, theme)
- [ ] Backup/restore views

## Phase 11 – Static Assets & Animations
- [ ] `static/css/main.css` (color palette, glassmorphism, animations)
- [ ] `static/js/three_hero.js` (Three.js scene)
- [ ] `static/js/dashboard.js` (Chart.js + GSAP)
- [ ] `static/js/pos.js` (Alpine.js cart)
- [ ] `static/js/sidebar.js` (responsive sidebar)
- [ ] `static/js/main.js` (global utilities)

## Phase 12 – Admin & Documentation
- [ ] Custom Django Admin for all models
- [ ] README.md
- [ ] requirements.txt (final)
- [ ] Sample data / fixtures
