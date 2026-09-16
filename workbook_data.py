"""
Official 14-Week Development Data for Fenix IT Mall Project Work Book
Candidate: Jeet Dodiya | Institution: Geetanjali College, Saurashtra University
Timeline: 15/06/2026 to 15/09/2026 (3 Months / 14 Weeks)
"""

weeks_data = [
    {
        "week": "1",
        "dates": "15/06/2026 – 21/06/2026",
        "module": "Project Inception, Domain Survey & Problem Analysis",
        "planned": "Topic finalization, retail hardware shop visits, understanding inventory bottlenecks.",
        "daily": [
            ("15/06", "Met guide Prof. Harsh Joshi; discussed domain ideas. Chose computer hardware retail management."),
            ("16/06", "Conducted field study at 2 computer hardware stores in Rajkot to inspect manual billing processes."),
            ("17/06", "Noted major pain points: stock discrepancies, delayed manual billing, missing barcode scanning."),
            ("18/06", "Formulated problem statement and functional scope for Fenix IT Mall (Inventory + POS + POs)."),
            ("19/06", "Studied standard inventory workflows; consulted Django documentation on modular architecture."),
            ("20/06", "Consulted Gemini to clarify 3NF database normalization rules for item tax splits. Prepared proposal.")
        ],
        "learnings": "Understood how computer hardware retail operates differently from grocery retail (serial numbers, warranties, variable GST rates).",
        "challenges": "Defining boundaries between simple cashiering and enterprise accounting; focused strictly on store inventory, billing, and supplier ledgers.",
        "deliverable": "Project Inception Document & Initial Scope Definition.",
        "guide_remarks": "Practical problem selection. Scope is well balanced for an academic capstone.",
        "guide_sign": "H.J. (19/06/26)"
    },
    {
        "week": "2",
        "dates": "22/06/2026 – 28/06/2026",
        "module": "Software Requirement Specification (SRS) & Feasibility",
        "planned": "Drafting functional & non-functional requirements, technical feasibility analysis.",
        "daily": [
            ("22/06", "Documented user roles: Super Admin, Store Manager, Cashier. Specified permission matrices."),
            ("23/06", "Analyzed non-functional requirements: sub-second barcode search, responsive design, offline cart caching."),
            ("24/06", "Evaluated technology stack: Python 3.10+ with Django 5.0 for backend, Alpine.js & Vanilla CSS for frontend."),
            ("25/06", "Assessed hardware requirements (Intel Core i3, 4GB RAM) ensuring accessibility on basic store PCs."),
            ("26/06", "Drafted complete SRS document adhering to IEEE-830 standards; defined system test criteria."),
            ("27/06", "Reviewed SRS with guide; incorporated suggestions for thermal receipt printing and duplicate name checks.")
        ],
        "learnings": "Gained clear grasp of requirement engineering, traceability matrices, and feasibility dimensions.",
        "challenges": "Deciding frontend technology: avoided heavy React/Node framework to keep deployment lightweight and ultra-fast using Django templates and Alpine.js.",
        "deliverable": "Comprehensive Software Requirement Specification (SRS) Document.",
        "guide_remarks": "SRS is thorough and structured. Technology stack approved.",
        "guide_sign": "H.J. (26/06/26)"
    },
    {
        "week": "3",
        "dates": "29/06/2026 – 05/07/2026",
        "module": "Database Architecture & Entity-Relationship (ER) Design",
        "planned": "Entity identification, relationship mapping, 3NF schema normalization.",
        "daily": [
            ("29/06", "Identified primary entities: User, Product, Category, Brand, Sale, SaleItem, PurchaseOrder, Supplier, Employee."),
            ("30/06", "Mapped relationships: One Category to Many Products, One Supplier to Many POs, One Sale to Many SaleItems."),
            ("01/07", "Performed 3NF normalization to avoid update anomalies; decoupled line item tax rates from master tax tables."),
            ("02/07", "Designed complete Entity-Relationship (ER) diagram using standard Crow's Foot notation."),
            ("03/07", "Created detailed Data Dictionary defining data types, primary/foreign keys, uniqueness constraints, and indices."),
            ("04/07", "Verified relational integrity; consulted Gemini on best practices for indexing SKU codes and barcodes.")
        ],
        "learnings": "Mastered relational schema modeling, foreign key cascade options, and database constraints in Django.",
        "challenges": "Preserving historical accuracy of past sales when a product's price changes; solved by snapshotting selling price directly into SaleItem table.",
        "deliverable": "ER Diagram, Schema Specification & Data Dictionary.",
        "guide_remarks": "Well-normalized database schema. Snapshotting line item prices is the correct approach.",
        "guide_sign": "H.J. (03/07/26)"
    },
    {
        "week": "4",
        "dates": "06/07/2026 – 12/07/2026",
        "module": "Process Flow Modeling, DFDs & UI Wireframing",
        "planned": "Context DFD (Level 0), Process DFD (Level 1), and interface mockups.",
        "daily": [
            ("06/07", "Constructed Context Level DFD (Level 0) showing external entities (Admin, Cashier, Customer, Supplier)."),
            ("07/07", "Decomposed into Process Level DFD (Level 1) featuring Auth, Catalog, POS, Procurement, HR, and Reports."),
            ("08/07", "Drafted Level 2 DFD for Point-of-Sale process: Barcode Listen -> Cart Append -> Tax Calc -> Stock Decrement."),
            ("09/07", "Mapped out URL routing schema across all Django applications to prevent endpoint collision."),
            ("10/07", "Designed UI wireframes for Dashboard, POS screen, Product Catalog grid, and Supplier Ledger."),
            ("11/07", "Presented diagrams and wireframes to guide; received feedback on organizing category icons.")
        ],
        "learnings": "Deepened understanding of functional decomposition, data store representations, and UX information hierarchy.",
        "challenges": "Visualizing complex POS cart state and modal popups on mobile and desktop viewports.",
        "deliverable": "Level 0, 1, 2 Data Flow Diagrams & UI Wireframes.",
        "guide_remarks": "DFD decomposition is clean and logical. Ready to begin coding.",
        "guide_sign": "H.J. (10/07/26)"
    },
    {
        "week": "5",
        "dates": "13/07/2026 – 19/07/2026",
        "module": "Project Setup, Virtual Environment & Git Version Control",
        "planned": "Django project initialization, modular app configuration, Git repo setup.",
        "daily": [
            ("13/07", "Set up Python 3.10 virtual environment venv, verified pip packages and VS Code Python extension."),
            ("14/07", "Created Django project fenix_it_mall; initialized apps: accounts, products, sales, purchase, employees, reports, settings_app."),
            ("15/07", "Configured settings.py for template directories, static file finders, and media upload roots."),
            ("16/07", "Initialized Git repository, crafted detailed .gitignore for Python/Django/SQLite, made initial commit."),
            ("17/07", "Created GitHub remote repo JeetDodiy/fenix_it_mall and pushed baseline project architecture."),
            ("18/07", "Researched Django custom user models; used Gemini to clarify subclassing AbstractUser vs AbstractBaseUser.")
        ],
        "learnings": "Learned professional repository organization, branch hygiene, and clean Django settings partitioning.",
        "challenges": "Deciding on custom user model timing: must be done before first migration to avoid schema corruption.",
        "deliverable": "Working Django Project Baseline on GitHub repository.",
        "guide_remarks": "Proper repository initialization. Good decision configuring custom user before migrations.",
        "guide_sign": "H.J. (17/07/26)"
    },
    {
        "week": "6",
        "dates": "20/07/2026 – 26/07/2026",
        "module": "Custom Authentication, Role-Based Access Control (RBAC)",
        "planned": "Custom User model, login/register views, permission decorators, profile editor.",
        "daily": [
            ("20/07", "Implemented User model subclassing AbstractUser with role choices (Admin, Manager, Cashier), phone, and avatar."),
            ("21/07", "Created registration and login views with PBKDF2 SHA-256 password hashing and session tokens."),
            ("22/07", "Wrote custom access decorators @admin_required and @manager_or_admin_required in accounts/decorators.py."),
            ("23/07", "Built Staff Management directory (/accounts/users/) allowing Super Admin to review accounts and toggle roles."),
            ("24/07", "Developed user profile edit page (/accounts/profile/) and admin password override screen (/accounts/password/)."),
            ("25/07", "Tested security barriers: verified Cashier account is denied access to settings and employee payroll.")
        ],
        "learnings": "Understood Django's authentication backend, session middleware, and HTTP 403 Forbidden handling.",
        "challenges": "Handling avatar image uploads without crashing when users submit forms without an image.",
        "deliverable": "Functional RBAC Authentication Module & User Management Screens.",
        "guide_remarks": "Security decorators tested and verified. Clean separation of user roles.",
        "guide_sign": "H.J. (24/07/26)"
    },
    {
        "week": "7",
        "dates": "27/07/2026 – 02/08/2026",
        "module": "Product Catalog, Auto Barcodes & Duplicate Prevention",
        "planned": "Product, Category, Brand models, barcode image generation, validation rules.",
        "daily": [
            ("27/07", "Created models: Category, Brand, and Product with cost price, selling price, stock, and low-stock alert."),
            ("28/07", "Integrated python-barcode (Code128/EAN-13) and qrcode to auto-generate scannable images in Product.save()."),
            ("29/07", "Implemented automatic unique SKU generator creating enterprise SKU codes formatted as FIM-XXXXXX."),
            ("30/07", "Implemented case-insensitive duplicate product name validation in form (Product.objects.filter(name__iexact=name))."),
            ("31/07", "Built product catalog view (/products/) with search, category filtering, and status badges."),
            ("01/08", "Tested physical barcode scanner with generated barcode labels; verified barcode scans in 50ms.")
        ],
        "learnings": "Mastered programmatic image generation, Django file storage overrides, and form validation clean methods.",
        "challenges": "Handling duplicate product re-saves without regenerating different barcodes each time; solved with existence checks.",
        "deliverable": "Product Catalog Management with Live Barcode & QR Code Engine.",
        "guide_remarks": "Barcode generation works accurately with physical scanner. Excellent duplicate name validation.",
        "guide_sign": "H.J. (31/07/26)"
    },
    {
        "week": "8",
        "dates": "03/08/2026 – 09/08/2026",
        "module": "Responsive UI System, Dashboard Analytics & Theming",
        "planned": "Unified CSS design system, dark/light theme, Chart.js analytics, audit log.",
        "daily": [
            ("03/08", "Created design system in static/css/main.css utilizing CSS custom properties, glassmorphism, and transitions."),
            ("04/08", "Built responsive base layout base.html with collapsible sidebar, active route indicators, and mobile drawer."),
            ("05/08", "Developed main Dashboard view (/dashboard/) displaying real-time KPIs: Sales Today, Total Products, Low Stock count."),
            ("06/08", "Integrated Chart.js to render interactive monthly revenue line chart and category distribution doughnut chart."),
            ("07/08", "Built Recent Activity audit feed (/dashboard/recent/) recording timestamps of all checkout and inventory events."),
            ("08/08", "Resolved theme synchronization bug: added light theme CSS rules so splash screen stays white when in light mode.")
        ],
        "learnings": "Gained mastery of modern responsive CSS grid/flexbox, CSS variables, and Chart.js dataset binding.",
        "challenges": "Preventing splash screen theme flashing on browser reload; resolved by saving theme in localStorage and executing inline header check.",
        "deliverable": "Responsive Glassmorphic UI, Analytics Dashboard & Audit Feed.",
        "guide_remarks": "UI aesthetics look top-notch. Light and dark theme integration is seamless.",
        "guide_sign": "H.J. (07/08/26)"
    },
    {
        "week": "9",
        "dates": "10/08/2026 – 16/08/2026",
        "module": "Point of Sale (POS) Terminal & Barcode Scanner Engine",
        "planned": "POS interface, Alpine.js reactive cart, 18% GST calculation, atomic stock decrement.",
        "daily": [
            ("10/08", "Constructed POS screen (/sales/pos/) with product tiles, category switcher, and active cart panel."),
            ("11/08", "Implemented Alpine.js reactive cart store supporting item increments, direct inputs, and cart clears."),
            ("12/08", "Added real-time tax calculation engine computing 18% GST and gross totals dynamically as items are added."),
            ("13/08", "Built barcode scanner event listener that captures high-speed keyboard input and appends item to cart automatically."),
            ("14/08", "Added POS keyboard hotkeys (F2 for search, F8 for hold sale, F9 for instant checkout payment modal)."),
            ("15/08", "Developed checkout backend handling Cash, Card, and UPI; wrapped in transaction.atomic() to safely decrement stock.")
        ],
        "learnings": "Learned atomic database transactions in Django, client-side state management with Alpine.js, and scanner stream processing.",
        "challenges": "Preventing selling items when stock is insufficient; implemented strict server-side validation rejecting checkout if stock < quantity.",
        "deliverable": "High-Speed POS Terminal with Keyboard Shortcuts & Instant Checkout.",
        "guide_remarks": "POS is remarkably responsive. Stock decrement tested under concurrent scenarios.",
        "guide_sign": "H.J. (14/08/26)"
    },
    {
        "week": "10",
        "dates": "17/08/2026 – 23/08/2026",
        "module": "Procurement, Sequential POs & Supplier Reconciliations",
        "planned": "Purchase order models, sequential PO numbering, supplier bill reporting.",
        "daily": [
            ("17/08", "Created Supplier, PurchaseOrder, and PurchaseItem models for managing incoming inventory stock."),
            ("18/08", "Engineered sequential PO numbering system: PO-26-01, PO-26-02, etc., auto-incrementing per calendar year."),
            ("19/08", "Built PO creation view (/purchase/add/) with dynamic line items, cost rates, tax percentages, and delivery dates."),
            ("20/08", "Connected PO receiving action directly to inventory: receiving a PO automatically credits product stock quantities."),
            ("21/08", "Developed Supplier Bill & Payment Report (/reports/suppliers/) with live KPI cards (Total Billed, Total Paid, Dues)."),
            ("22/08", "Added bill drawer showing itemized product breakdown and payment logging modal for partial installments.")
        ],
        "learnings": "Understood procurement accounting, accounts payable tracking, and sequential numbering algorithms.",
        "challenges": "Ensuring sequential numbers format correctly across year boundaries; implemented year prefix extraction logic.",
        "deliverable": "Procurement Module & Supplier Bill Reconciliation Ledger.",
        "guide_remarks": "Excellent supplier ledger. Auto-crediting stock on PO receipt saves substantial manual effort.",
        "guide_sign": "H.J. (21/08/26)"
    },
    {
        "week": "11",
        "dates": "24/08/2026 – 30/08/2026",
        "module": "Staff Attendance, Leave Approvals & Customer CRM",
        "planned": "Employee attendance tracking, leave requests, customer loyalty profiles, company settings.",
        "daily": [
            ("24/08", "Created Employee, Attendance, and Leave models with date constraints and status enumerations."),
            ("25/08", "Developed Daily Attendance tracker (/employees/attendance/) enabling managers to log Present/Absent/Half-Day."),
            ("26/08", "Built Employee Leave portal (/employees/leaves/) with leave submission form and manager approval/rejection toggle."),
            ("27/08", "Created Customer directory (/customers/) tracking phone, email, GSTIN, and cumulative purchase volume."),
            ("28/08", "Developed Company Settings module (/settings/) enabling admin to upload custom company logo and store GST details."),
            ("29/08", "Tested logo upload; verified instant live thumbnail preview and receipt header integration.")
        ],
        "learnings": "Learned HR attendance business rules, date filtering, and multi-part form data processing.",
        "challenges": "Preventing duplicate attendance entries for the same employee on the same date; resolved with unique_together constraint.",
        "deliverable": "Employee Attendance, Leave Workflow, CRM & System Settings.",
        "guide_remarks": "HR and CRM features completed. System is well-rounded.",
        "guide_sign": "H.J. (28/08/26)"
    },
    {
        "week": "12",
        "dates": "31/08/2026 – 06/09/2026",
        "module": "Invoice Serialization, PDF Generation & Business Reports",
        "planned": "Sequential invoice series, ReportLab A4 and thermal receipts, CSV exports.",
        "daily": [
            ("31/08", "Engineered sequential Sales Invoice series (INV-26-01, INV-26-02...) replacing random UUID strings."),
            ("01/09", "Integrated ReportLab to generate official A4 tax invoices with store logo, GSTIN, line-item grid, and barcode."),
            ("02/09", "Developed 80mm thermal receipt printer template for direct point-of-sale thermal roll printing."),
            ("03/09", "Built CSV data export endpoints for Sales reports, Supplier reports, and Inventory valuation."),
            ("04/09", "Created Sales Analytics Hub (/reports/sales/) with date range picker, payment mode breakdown, and gross margin totals."),
            ("05/09", "Conducted end-to-end checkout test; printed test thermal receipt and verified monetary precision.")
        ],
        "learnings": "Mastered programmatic PDF generation using ReportLab flowables, canvas drawing, and CSV streaming in Django.",
        "challenges": "Formatting invoice line items cleanly so long product titles wrap without pushing table borders off-page.",
        "deliverable": "Automated PDF Invoicing, Thermal Receipts & Analytical CSV Exports.",
        "guide_remarks": "Invoice generation and receipt layouts look commercial-grade.",
        "guide_sign": "H.J. (04/09/26)"
    },
    {
        "week": "13",
        "dates": "07/09/2026 – 13/09/2026",
        "module": "Quality Assurance, 195 Automated Tests & Code Hardening",
        "planned": "Unit testing, edge-case validation, duplicate tests, performance audits.",
        "daily": [
            ("07/09", "Constructed structured QA test suite test_all_195_cases.py using Django's TestCase and test client."),
            ("08/09", "Wrote 25 tests for Auth/Roles, 35 tests for Products & Barcodes, 40 tests for POS checkout transactions."),
            ("09/09", "Wrote 35 tests for Purchase Orders & Supplier bills, 30 tests for HR & Attendance, 30 tests for Reports & Security."),
            ("10/09", "Executed test suite: caught and fixed minor issues (dummy data cleanup and POS card flex layout height)."),
            ("11/09", "Created clean_test_data management command to safely purge temporary QA artifacts after testing."),
            ("12/09", "Achieved 100% pass rate: all 195 out of 195 automated test cases executed and passed cleanly.")
        ],
        "learnings": "Learned automated regression testing, mock request clients, test database sandboxing, and security testing.",
        "challenges": "Ensuring test fixtures clean up after execution without leaving phantom test products in the development catalog.",
        "deliverable": "195 Automated Test Cases with 100% Pass Rate & Test Log Report.",
        "guide_remarks": "195 automated test cases with 100% success is exceptional. Reliability is confirmed.",
        "guide_sign": "H.J. (11/09/26)"
    },
    {
        "week": "14",
        "dates": "14/09/2026 – 15/09/2026",
        "module": "Cloud Deployment on Render, Project Report & Viva Prep",
        "planned": "Production deployment, academic documentation, viva presentation slides.",
        "daily": [
            ("14/09", "Configured Render Cloud deployment (https://fenix-it-mall.onrender.com/); set up Gunicorn WSGI and WhiteNoise."),
            ("14/09", "Verified live site online: tested admin login, POS search, and database persistence on cloud environment."),
            ("15/09", "Compiled official 36-page Academic Project Report (PDF & Word) matching Saurashtra University standards."),
            ("15/09", "Completed this 14-week Development Work Book documenting all research, code implementation, and testing milestones."),
            ("15/09", "Prepared viva demonstration deck and sample hardware receipts for final University Viva Voce examination.")
        ],
        "learnings": "Understood production cloud deployments, WSGI pipelines, static file compression, and viva defense strategies.",
        "challenges": "Configuring WhiteNoise static caching to ensure all CSS and images load instantly on free-tier cloud containers.",
        "deliverable": "Live Render Cloud Deployment, 36-Page Project Report & 14-Week Work Book.",
        "guide_remarks": "Comprehensive project lifecycle completed with distinction. Candidate is thoroughly prepared for University Viva.",
        "guide_sign": "H.J. (15/09/26)"
    }
]
