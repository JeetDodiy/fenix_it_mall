import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('docs_assets', exist_ok=True)

def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 95, "Fenix IT Mall — 3-Tier Enterprise Architecture", ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#1e293b')
    
    # Tier 1: Client Layer
    rect1 = patches.FancyBboxPatch((5, 65), 90, 22, boxstyle="round,pad=1", ec="#3b82f6", fc="#eff6ff", lw=2)
    ax.add_patch(rect1)
    ax.text(10, 83, "PRESENTATION TIER (CLIENT)", fontsize=11, fontweight='bold', color="#1d4ed8")
    ax.text(50, 74, "Modern Web Browser / Mobile / POS Scanner Station\nHTML5 + Vanilla CSS3 Glassmorphism + Alpine.js Real-Time Reactive UI", 
            ha='center', va='center', fontsize=9, color="#1e3a8a")
    
    # Arrow 1
    ax.annotate('', xy=(50, 58), xytext=(50, 65),
                arrowprops=dict(arrowstyle="<->", color="#2563eb", lw=2))
    ax.text(52, 61.5, "HTTPS / REST / AJAX / Static Assets", fontsize=8, color="#475569")
    
    # Tier 2: Application Layer
    rect2 = patches.FancyBboxPatch((5, 30), 90, 26, boxstyle="round,pad=1", ec="#10b981", fc="#ecfdf5", lw=2)
    ax.add_patch(rect2)
    ax.text(10, 52, "APPLICATION & BUSINESS LOGIC TIER (RENDER CLOUD)", fontsize=11, fontweight='bold', color="#047857")
    
    # Sub-boxes in App Layer
    ax.text(22, 42, "Gunicorn WSGI Server\n& WhiteNoise Engine", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc="#d1fae5", ec="#059669"), fontsize=8, color="#064e3b")
    ax.text(50, 42, "Django 5.0 Core (MVT)\nAuth, POS, Inventory, HR", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc="#d1fae5", ec="#059669"), fontsize=8, color="#064e3b")
    ax.text(78, 42, "ReportLab & Utility Libs\nPDF, Barcode, QR Generation", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc="#d1fae5", ec="#059669"), fontsize=8, color="#064e3b")
    
    # Arrow 2
    ax.annotate('', xy=(50, 22), xytext=(50, 30),
                arrowprops=dict(arrowstyle="<->", color="#059669", lw=2))
    ax.text(52, 26, "Django ORM Queries (ACID Transactions)", fontsize=8, color="#475569")
    
    # Tier 3: Data Layer
    rect3 = patches.FancyBboxPatch((5, 3), 90, 18, boxstyle="round,pad=1", ec="#8b5cf6", fc="#f5f3ff", lw=2)
    ax.add_patch(rect3)
    ax.text(10, 17, "DATA & STORAGE TIER", fontsize=11, fontweight='bold', color="#6d28d9")
    ax.text(32, 10, "SQLite3 / PostgreSQL Relational DB\n(Catalog, Orders, Ledgers, Users)", ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="#ede9fe", ec="#7c3aed"), fontsize=8, color="#4c1d95")
    ax.text(75, 10, "Media & Asset Storage\n(Company Logos, Product Images)", ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="#ede9fe", ec="#7c3aed"), fontsize=8, color="#4c1d95")
    
    plt.tight_layout()
    plt.savefig('docs_assets/diagram_system_architecture.png', dpi=300)
    plt.close()
    print("Architecture diagram created.")

def generate_dfd_level_0():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 94, "Data Flow Diagram (DFD Level 0 — Context Level)", ha='center', va='center',
            fontsize=15, fontweight='bold', color='#1e293b')
    
    # Central Process
    circ = patches.Circle((50, 50), 18, ec="#2563eb", fc="#dbeafe", lw=2.5)
    ax.add_patch(circ)
    ax.text(50, 52, "0.0", ha='center', va='center', fontsize=12, fontweight='bold', color="#1e40af")
    ax.text(50, 47, "Fenix IT Mall\nPOS & ERP\nSystem", ha='center', va='center', fontsize=10, fontweight='bold', color="#1e3a8a")
    
    # External Entities
    entities = [
        ("Admin / Manager", (15, 80), "#f59e0b", "#fef3c7"),
        ("Cashier", (15, 20), "#10b981", "#ecfdf5"),
        ("Customer", (85, 80), "#8b5cf6", "#f5f3ff"),
        ("Supplier", (85, 20), "#ef4444", "#fef2f2")
    ]
    
    for name, pos, ec, fc in entities:
        rect = patches.FancyBboxPatch((pos[0]-12, pos[1]-7), 24, 14, boxstyle="round,pad=0.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], name, ha='center', va='center', fontsize=9, fontweight='bold', color="#1f2937")
        
    # Flow Admin -> Central
    ax.annotate("Config, Products, HR", xy=(35, 60), xytext=(22, 73),
                arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.5), fontsize=8)
    ax.annotate("Analytics & Reports", xy=(24, 75), xytext=(38, 63),
                arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.5), fontsize=8)
    
    # Flow Cashier -> Central
    ax.annotate("POS Checkout / Scan", xy=(36, 40), xytext=(22, 27),
                arrowprops=dict(arrowstyle="->", color="#047857", lw=1.5), fontsize=8)
    ax.annotate("Receipt Print / Stock", xy=(22, 24), xytext=(38, 37),
                arrowprops=dict(arrowstyle="->", color="#047857", lw=1.5), fontsize=8)
    
    # Flow Customer -> Central
    ax.annotate("Payment / Orders", xy=(64, 60), xytext=(78, 73),
                arrowprops=dict(arrowstyle="->", color="#6d28d9", lw=1.5), fontsize=8)
    ax.annotate("Invoice / Points", xy=(76, 75), xytext=(62, 63),
                arrowprops=dict(arrowstyle="->", color="#6d28d9", lw=1.5), fontsize=8)
                
    # Flow Supplier -> Central
    ax.annotate("Goods & Invoices", xy=(64, 40), xytext=(78, 27),
                arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.5), fontsize=8)
    ax.annotate("Purchase Order / Pay", xy=(76, 24), xytext=(62, 37),
                arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.5), fontsize=8)

    plt.tight_layout()
    plt.savefig('docs_assets/diagram_dfd_level_0.png', dpi=300)
    plt.close()
    print("DFD 0 created.")

def generate_dfd_level_1():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 96, "Data Flow Diagram (DFD Level 1 — Core Processes)", ha='center', va='center',
            fontsize=15, fontweight='bold', color='#1e293b')
            
    procs = [
        ("1.0\nUser Auth &\nAccess Control", (20, 75), "#3b82f6", "#eff6ff"),
        ("2.0\nCatalog &\nBarcode Engine", (50, 75), "#10b981", "#ecfdf5"),
        ("3.0\nPOS Checkout\n& Invoicing", (80, 75), "#8b5cf6", "#f5f3ff"),
        ("4.0\nProcurement &\nSupplier Ledger", (30, 25), "#f59e0b", "#fef3c7"),
        ("5.0\nAnalytics &\nFinancial Reports", (70, 25), "#ec4899", "#fdf2f8")
    ]
    
    for label, pos, ec, fc in procs:
        circ = patches.Circle(pos, 12, ec=ec, fc=fc, lw=2)
        ax.add_patch(circ)
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=8, fontweight='bold', color="#1f2937")
        
    # Central Data Store
    rect = patches.FancyBboxPatch((35, 46), 30, 10, boxstyle="square,pad=0.2", ec="#475569", fc="#f8fafc", lw=2)
    ax.add_patch(rect)
    ax.text(50, 51, "D1: Fenix Central Database (SQLite/Postgres)", ha='center', va='center',
            fontsize=9, fontweight='bold', color="#0f172a")
            
    # Connect processes to DB
    ax.annotate('', xy=(30, 56), xytext=(24, 63), arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.5))
    ax.annotate('', xy=(50, 56), xytext=(50, 63), arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.5))
    ax.annotate('', xy=(70, 56), xytext=(76, 63), arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.5))
    ax.annotate('', xy=(40, 46), xytext=(35, 37), arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.5))
    ax.annotate('', xy=(60, 46), xytext=(65, 37), arrowprops=dict(arrowstyle="<->", color="#475569", lw=1.5))

    plt.tight_layout()
    plt.savefig('docs_assets/diagram_dfd_level_1.png', dpi=300)
    plt.close()
    print("DFD 1 created.")

def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 96, "Entity Relationship (ER) Diagram", ha='center', va='center',
            fontsize=16, fontweight='bold', color='#1e293b')
            
    entities = [
        ("CustomUser\n- id (PK)\n- username\n- role flags", (15, 80), "#3b82f6", "#eff6ff"),
        ("Category\n- id (PK)\n- name (unique)\n- image", (40, 80), "#10b981", "#ecfdf5"),
        ("Brand\n- id (PK)\n- name (unique)\n- logo", (65, 80), "#10b981", "#ecfdf5"),
        ("Supplier\n- id (PK)\n- name, phone\n- gstin, balance", (90, 80), "#f59e0b", "#fef3c7"),
        
        ("Product\n- id (PK)\n- name (unique)\n- code, barcode\n- stock_qty, price", (50, 52), "#6366f1", "#eef2ff"),
        
        ("Sale / Invoice\n- id (PK)\n- invoice_no\n- grand_total, date", (20, 20), "#ec4899", "#fdf2f8"),
        ("SaleItem\n- id (PK)\n- product_id (FK)\n- qty, unit_price", (45, 20), "#ec4899", "#fdf2f8"),
        ("PurchaseOrder\n- id (PK)\n- order_no (PO-YY)\n- total, paid_amt", (75, 20), "#f59e0b", "#fef3c7"),
        ("SupplierPayment\n- id (PK)\n- po_id (FK)\n- amount, method", (92, 20), "#f59e0b", "#fef3c7")
    ]
    
    for name, pos, ec, fc in entities:
        w, h = 18, 14
        rect = patches.FancyBboxPatch((pos[0]-w/2, pos[1]-h/2), w, h, boxstyle="round,pad=0.3", ec=ec, fc=fc, lw=1.5)
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], name, ha='center', va='center', fontsize=7.5, fontweight='bold', color="#1f2937")

    # Connect lines
    ax.annotate("1 : N", xy=(46, 59), xytext=(42, 73), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2), fontsize=7)
    ax.annotate("1 : N", xy=(54, 59), xytext=(63, 73), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2), fontsize=7)
    ax.annotate("1 : N", xy=(59, 57), xytext=(83, 73), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.2), fontsize=7)
    ax.annotate("1 : N", xy=(29, 20), xytext=(36, 20), arrowprops=dict(arrowstyle="<->", color="#db2777", lw=1.2), fontsize=7)
    ax.annotate("FK", xy=(48, 45), xytext=(46, 27), arrowprops=dict(arrowstyle="->", color="#4f46e5", lw=1.2), fontsize=7)
    ax.annotate("1 : N", xy=(84, 20), xytext=(83, 20), arrowprops=dict(arrowstyle="<->", color="#d97706", lw=1.2), fontsize=7)
    ax.annotate("1 : N", xy=(78, 27), xytext=(88, 73), arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.2), fontsize=7)

    plt.tight_layout()
    plt.savefig('docs_assets/diagram_er_model.png', dpi=300)
    plt.close()
    print("ER diagram created.")

def generate_pos_workflow():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 94, "High-Speed POS Checkout State Workflow", ha='center', va='center',
            fontsize=15, fontweight='bold', color='#1e293b')
            
    steps = [
        ("1. Scan / Search\nBarcode Scanner (Enter)\nor F2 Instant Filter", (15, 60), "#3b82f6", "#eff6ff"),
        ("2. Add to Cart\nSelect Product &\nAdjust Quantities", (38, 60), "#10b981", "#ecfdf5"),
        ("3. Hold Sale (F8)\nor Resume Cart\n(Local Storage Cache)", (38, 20), "#f59e0b", "#fef3c7"),
        ("4. Payment Select\nCash / Card / UPI\nAuto 18% GST Calc", (62, 60), "#8b5cf6", "#f5f3ff"),
        ("5. Atomic Checkout\nStock Decrement\n& INV-26-XX Create", (85, 60), "#ec4899", "#fdf2f8"),
        ("6. Receipt Print\nA4 or Thermal\nPrintable Slip", (85, 20), "#06b6d4", "#ecfeff")
    ]
    
    for title, pos, ec, fc in steps:
        rect = patches.FancyBboxPatch((pos[0]-10, pos[1]-8), 20, 16, boxstyle="round,pad=0.4", ec=ec, fc=fc, lw=1.8)
        ax.add_patch(rect)
        ax.text(pos[0], pos[1], title, ha='center', va='center', fontsize=8, fontweight='bold', color="#1f2937")
        
    # Arrows
    ax.annotate('', xy=(28, 60), xytext=(25, 60), arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=2))
    ax.annotate('', xy=(38, 52), xytext=(38, 28), arrowprops=dict(arrowstyle="<->", color="#f59e0b", lw=2))
    ax.annotate('', xy=(52, 60), xytext=(48, 60), arrowprops=dict(arrowstyle="->", color="#10b981", lw=2))
    ax.annotate('', xy=(75, 60), xytext=(72, 60), arrowprops=dict(arrowstyle="->", color="#8b5cf6", lw=2))
    ax.annotate('', xy=(85, 28), xytext=(85, 52), arrowprops=dict(arrowstyle="->", color="#ec4899", lw=2))

    plt.tight_layout()
    plt.savefig('docs_assets/diagram_pos_workflow.png', dpi=300)
    plt.close()
    print("POS workflow created.")

if __name__ == '__main__':
    generate_system_architecture()
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_er_diagram()
    generate_pos_workflow()
    print("All architectural diagrams rendered successfully!")
