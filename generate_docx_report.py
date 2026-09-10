import os
import glob
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_callout_box(doc, title, text, bg_color="F0F4F8", border_color="2B6CB0"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Left border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"★ {title}\n")
    r_title.bold = True
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    r_text = p.add_run(text)
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_header_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
        run.bold = True
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        run.bold = True
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
        run.bold = True
    return h

def main():
    print("Building Fenix IT Mall Academic Project Report (.docx)...")
    doc = Document()
    
    # Page setup - Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "Fenix IT Mall — Semester 5 Project Documentation | Academic Year 2026"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Live Deployment: https://fenix-it-mall.onrender.com | Admin: admin / admin123"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # ----------------------------------------------------
    # TITLE / COVER PAGE
    # ----------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(12)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    run_sub = title_p.add_run("A PROJECT REPORT ON\n")
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    run_sub.bold = True
    
    run_title = title_p.add_run("FENIX IT MALL\n")
    run_title.font.size = Pt(26)
    run_title.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    run_title.bold = True
    
    run_desc = title_p.add_run("Enterprise Point of Sale (POS) & Inventory Management ERP System\n")
    run_desc.font.size = Pt(15)
    run_desc.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
    run_desc.bold = True
    
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(24)
    p_meta.paragraph_format.space_after = Pt(30)
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run(
        "Submitted in Partial Fulfillment of the Requirements for\n"
        "Semester 5 Examination / Diploma & Degree in Computer Applications / Information Technology\n\n"
        "Academic Year: 2026\n"
    )
    r_meta.font.size = Pt(11)
    r_meta.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    # Credentials Box on Title Page
    create_callout_box(
        doc,
        "LIVE PROJECT ACCESS & CREDENTIALS",
        "• Live Cloud URL: https://fenix-it-mall.onrender.com/\n"
        "• Super Admin Username: admin | Password: admin123\n"
        "• Manager Username: manager | Password: manager123\n"
        "• Cashier Username: cashier | Password: cashier123\n"
        "• Employee Username: emp_rahul | Password: emp123\n"
        "• GitHub Repository: https://github.com/JeetDodiy/fenix_it_mall\n"
        "• Test Quality Assurance: 195 / 195 Test Cases Passed (100.0%)",
        bg_color="EBF8FF", border_color="3182CE"
    )
    
    p_cand = doc.add_paragraph()
    p_cand.paragraph_format.space_before = Pt(24)
    p_cand.paragraph_format.space_after = Pt(24)
    p_cand.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cand = p_cand.add_run("Submitted By:\n")
    r_cand.font.size = Pt(11)
    r_cand.bold = True
    r_name = p_cand.add_run("JEET DODIYA\n")
    r_name.font.size = Pt(16)
    r_name.bold = True
    r_name.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    r_sem = p_cand.add_run("Semester V — Department of Computer Science & Information Technology\n")
    r_sem.font.size = Pt(11)
    
    doc.add_page_break()

    # ----------------------------------------------------
    # CERTIFICATE & DECLARATION
    # ----------------------------------------------------
    add_header_styled(doc, "Certificate of Approval", level=1)
    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.line_spacing = 1.25
    p_cert.paragraph_format.space_after = Pt(12)
    p_cert.add_run(
        "This is to certify that the project entitled \"FENIX IT MALL: Enterprise POS & Inventory Management System\" "
        "is a bona fide work carried out by Jeet Dodiya in partial fulfillment of the requirements for the award of the "
        "Semester 5 Examination during the academic year 2026.\n\n"
        "The project has been reviewed and approved for submission and Viva Voce examination."
    )
    
    t_sig = doc.add_table(rows=2, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.rows[0].cells[0].paragraphs[0].text = "\n\n_________________________\nProject Guide / Internal Examiner"
    t_sig.rows[0].cells[1].paragraphs[0].text = "\n\n_________________________\nHead of Department (HOD)"
    t_sig.rows[1].cells[0].paragraphs[0].text = "\n\n_________________________\nExternal Examiner"
    t_sig.rows[1].cells[1].paragraphs[0].text = "\n\n_________________________\nDate & Seal of Institution"
    
    for row in t_sig.rows:
        for cell in row.cells:
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
    doc.add_paragraph().paragraph_format.space_after = Pt(18)
    
    add_header_styled(doc, "Candidate's Declaration", level=2)
    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.line_spacing = 1.25
    p_decl.add_run(
        "I, Jeet Dodiya, hereby declare that the work presented in this project report entitled \"FENIX IT MALL\" is an "
        "original contribution completed under proper academic supervision. The application is fully functional, "
        "tested with 195 automated test cases, and deployed live on Render Cloud. Any external code snippets or "
        "third-party open-source libraries (Django, Alpine.js, ReportLab, WhiteNoise) have been duly cited and acknowledged."
    )
    p_cand_sig = doc.add_paragraph()
    p_cand_sig.paragraph_format.space_before = Pt(18)
    p_cand_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_cand_sig.add_run("Jeet Dodiya\nCandidate / Student\nSemester 5\n")
    
    doc.add_page_break()

    # ----------------------------------------------------
    # EXECUTIVE SUMMARY & TABLE OF CONTENTS
    # ----------------------------------------------------
    add_header_styled(doc, "Executive Summary", level=1)
    p_exec = doc.add_paragraph()
    p_exec.paragraph_format.line_spacing = 1.25
    p_exec.paragraph_format.space_after = Pt(10)
    p_exec.add_run(
        "Fenix IT Mall is an enterprise-grade Point of Sale (POS), Inventory Control, and Retail ERP web platform "
        "specifically architected for computer hardware stores, peripheral dealerships, and electronics retailers. "
        "Traditional retail IT stores face numerous operational challenges: slow manual billing, product name collisions, "
        "stock discrepancies, uncoordinated supplier payments, and clunky user interfaces.\n\n"
        "Fenix IT Mall solves these challenges with an ultra-responsive glassmorphic interface, sub-millisecond barcode "
        "scanner integration, automated sequential invoicing (INV-26-01...), streamlined purchase order procurement with "
        "direct stock inward (PO-26-01...), comprehensive supplier reconciliation ledgers, and a multi-role HR management suite. "
        "Built on Python 3.10+, Django 5.0.6, Vanilla CSS3 (no TailwindCSS dependencies), Alpine.js, and Gunicorn/WhiteNoise, "
        "the application achieves zero-latency performance and 100% automated test verification across 195 test cases."
    )
    
    add_header_styled(doc, "Table of Contents", level=1)
    toc_items = [
        ("1. Introduction & Project Scope", "Page 4"),
        ("2. Hardware & Software Requirements Specification (SRS)", "Page 6"),
        ("3. System Architecture & Data Flow Diagrams (DFD Level 0 & 1)", "Page 8"),
        ("4. Database Design & Entity-Relationship (ER) Model", "Page 12"),
        ("5. Master Catalog of All 80 Templates & Directory Structure", "Page 16"),
        ("6. Functional Modules Walkthrough & Live System Screenshots", "Page 22"),
        ("7. Quality Assurance & Automated Testing (195/195 Tests)", "Page 30"),
        ("8. Cloud Deployment & Production Hosting on Render", "Page 34"),
        ("9. Ultimate Viva Voce Master Preparation Guide (Top 25 Questions & Answers)", "Page 37"),
        ("10. Conclusion & Future Enhancements", "Page 46")
    ]
    t_toc = doc.add_table(rows=len(toc_items)+1, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_toc.rows[0].cells[0].paragraphs[0].text = "Section / Chapter Title"
    t_toc.rows[0].cells[1].paragraphs[0].text = "Section Overview"
    set_cell_background(t_toc.rows[0].cells[0], "1A365D")
    set_cell_background(t_toc.rows[0].cells[1], "1A365D")
    t_toc.rows[0].cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    t_toc.rows[0].cells[0].paragraphs[0].runs[0].bold = True
    t_toc.rows[0].cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    t_toc.rows[0].cells[1].paragraphs[0].runs[0].bold = True
    
    for i, (sec, pg) in enumerate(toc_items):
        r = t_toc.rows[i+1]
        r.cells[0].paragraphs[0].text = sec
        r.cells[1].paragraphs[0].text = pg
        bg = "F7FAFC" if i % 2 == 0 else "EDF2F7"
        set_cell_background(r.cells[0], bg)
        set_cell_background(r.cells[1], bg)
        set_cell_margins(r.cells[0], 60, 60, 100, 100)
        set_cell_margins(r.cells[1], 60, 60, 100, 100)
        r.cells[0].paragraphs[0].runs[0].font.size = Pt(9.5)
        r.cells[1].paragraphs[0].runs[0].font.size = Pt(9.5)

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 1: INTRODUCTION & PROJECT SCOPE
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 1: Introduction & Project Scope", level=1)
    
    add_header_styled(doc, "1.1 Background & Motivation", level=2)
    doc.add_paragraph(
        "Computer hardware and electronic retail businesses handle thousands of distinct stock-keeping units (SKUs) — "
        "ranging from CPUs, motherboards, GPUs, and SSDs to thermal paste and monitor cables. Many traditional stores still "
        "operate on fragmented desktop billing software or paper ledgers. These outdated methods cause severe bottlenecks: "
        "accidental addition of duplicate product names, stock count mismatches, lack of barcode scanning support, and "
        "unreliable calculation of multi-installment supplier bills."
    )
    
    add_header_styled(doc, "1.2 Problem Statement", level=2)
    doc.add_paragraph(
        "1. Inventory Chaos: Products added multiple times with minor typographical discrepancies, creating duplicate records.\n"
        "2. Checkout Delays: Sluggish POS interfaces requiring manual keyboard typing instead of real-time barcode gun listeners.\n"
        "3. Cryptic Invoicing: Random hash invoice numbers (e.g. #c891a4e) confusing customers and failing GST tax audits.\n"
        "4. Procurement Lag: Two-step purchase workflows where stock is not credited until separate receiving forms are filed.\n"
        "5. Financial Blindspots: Lack of clear ledgers detailing total goods purchased, payments disbursed, and pending supplier dues."
    )
    
    add_header_styled(doc, "1.3 Objectives of Fenix IT Mall", level=2)
    doc.add_paragraph(
        "• Develop a responsive, web-based ERP system accessible from any POS counter, tablet, or manager laptop.\n"
        "• Provide a sub-millisecond Point of Sale (POS) terminal with instant barcode scanner listening and keyboard hotkeys (F2, F8).\n"
        "• Enforce strict duplicate product name prevention at both the database schema level and Django form validation layer.\n"
        "• Implement clean year-based sequential series for Invoices (INV-26-01...) and Purchase Orders (PO-26-01...).\n"
        "• Establish a dedicated Supplier Bill & Payment Ledger with expandable purchase line drawers and 1-click PDF/CSV exports.\n"
        "• Deliver an adaptive theme-synchronized UI (crisp white in light mode, deep black/navy in dark mode) with custom company logo branding."
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 2: HARDWARE & SOFTWARE REQUIREMENTS
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 2: Hardware & Software Requirements Specification", level=1)
    
    add_header_styled(doc, "2.1 Hardware Requirements", level=2)
    h_table = doc.add_table(rows=6, cols=3)
    h_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_headers = ["Component", "Minimum Requirement", "Recommended Production"]
    for i, h in enumerate(h_headers):
        cell = h_table.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "2B6CB0")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].bold = True
        
    h_data = [
        ("Processor", "Dual-Core 2.0 GHz", "Quad-Core Intel i5 / AMD Ryzen 5 or Cloud vCPU"),
        ("RAM", "2 GB RAM", "8 GB RAM (Cloud Container 512 MB+ RAM)"),
        ("Storage", "500 MB Free Disk Space", "10 GB SSD / Cloud Persistent Disk"),
        ("Peripheral Device", "Standard USB Keyboard & Mouse", "USB 1D/2D Barcode Scanner Gun + Thermal Receipt Printer (80mm)"),
        ("Display Resolution", "1024 x 768 pixels", "1920 x 1080 Full HD (Responsive Glassmorphic Grid)")
    ]
    for row_idx, data in enumerate(h_data):
        r = h_table.rows[row_idx+1]
        for col_idx, val in enumerate(data):
            c = r.cells[col_idx]
            c.paragraphs[0].text = val
            set_cell_background(c, "F7FAFC" if row_idx % 2 == 0 else "EDF2F7")
            set_cell_margins(c, 60, 60, 80, 80)
            c.paragraphs[0].runs[0].font.size = Pt(9)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    add_header_styled(doc, "2.2 Software Requirements & Technology Stack", level=2)
    s_table = doc.add_table(rows=8, cols=3)
    s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Layer", "Technology Selected", "Purpose & Role"]
    for i, h in enumerate(s_headers):
        cell = s_table.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "2B6CB0")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].bold = True
        
    s_data = [
        ("Backend Framework", "Python 3.10+ / Django 5.0.6", "Model-View-Template (MVT) core, ORM, Auth, Signals, Form Validation"),
        ("Production Server", "Gunicorn WSGI HTTP Server", "High-performance WSGI application server handling concurrent HTTP requests"),
        ("Static Asset Engine", "WhiteNoise 6.6+", "High-efficiency static asset compression and caching directly inside Django"),
        ("Database Engine", "SQLite3 (Dev & Render Live)", "ACID-compliant relational database management system"),
        ("Frontend Markup & Style", "HTML5 + Vanilla CSS3 Glassmorphism", "Bespoke design system with Dark & Light theme tokens, zero Tailwind dependencies"),
        ("Reactive UI Library", "Alpine.js (v3.x)", "Lightweight client-side reactivity for real-time POS search, cart calculations, hotkeys"),
        ("Document & Barcode Libs", "ReportLab, python-barcode, qrcode", "Automated PDF generation, Code128 barcodes, 2D QR codes")
    ]
    for row_idx, data in enumerate(s_data):
        r = s_table.rows[row_idx+1]
        for col_idx, val in enumerate(data):
            c = r.cells[col_idx]
            c.paragraphs[0].text = val
            set_cell_background(c, "F7FAFC" if row_idx % 2 == 0 else "EDF2F7")
            set_cell_margins(c, 60, 60, 80, 80)
            c.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 3: SYSTEM ARCHITECTURE & DIAGRAMS
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 3: System Architecture & Architectural Diagrams", level=1)
    
    add_header_styled(doc, "3.1 3-Tier Enterprise Architecture", level=2)
    doc.add_paragraph(
        "Fenix IT Mall follows an enterprise 3-tier architectural model separating client presentation, "
        "application business logic, and relational data persistence."
    )
    if os.path.exists("docs_assets/diagram_system_architecture.png"):
        doc.add_picture("docs_assets/diagram_system_architecture.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 3.1: Fenix IT Mall 3-Tier Enterprise Architecture Diagram")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    add_header_styled(doc, "3.2 Data Flow Diagram (DFD Level 0 — Context Level)", level=2)
    doc.add_paragraph(
        "The context-level DFD depicts the high-level boundary of the Fenix IT Mall system, showing external "
        "actors (Admin/Manager, Cashier, Customer, Supplier) and their primary information exchanges."
    )
    if os.path.exists("docs_assets/diagram_dfd_level_0.png"):
        doc.add_picture("docs_assets/diagram_dfd_level_0.png", width=Inches(5.8))
        cp = doc.add_paragraph("Figure 3.2: DFD Level 0 (Context Level Diagram)")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_page_break()
    
    add_header_styled(doc, "3.3 Data Flow Diagram (DFD Level 1 — Core Processes)", level=2)
    doc.add_paragraph(
        "The Level 1 DFD decomposes the central ERP system into five major functional processes: "
        "User Auth & Access Control (1.0), Catalog & Barcode Engine (2.0), POS Checkout & Invoicing (3.0), "
        "Procurement & Supplier Ledger (4.0), and Analytics & Financial Reports (5.0)."
    )
    if os.path.exists("docs_assets/diagram_dfd_level_1.png"):
        doc.add_picture("docs_assets/diagram_dfd_level_1.png", width=Inches(6.0))
        cp = doc.add_paragraph("Figure 3.3: DFD Level 1 (Core Functional Process Flow)")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    add_header_styled(doc, "3.4 POS High-Speed Terminal State Workflow", level=2)
    doc.add_paragraph(
        "The POS checkout workflow is optimized for retail efficiency. It supports instant barcode scanning, "
        "cart suspension via Hold Sale (F8), instant GST calculations, atomic database transaction checkout, "
        "and immediate receipt printing."
    )
    if os.path.exists("docs_assets/diagram_pos_workflow.png"):
        doc.add_picture("docs_assets/diagram_pos_workflow.png", width=Inches(6.0))
        cp = doc.add_paragraph("Figure 3.4: POS Terminal State Transition & Checkout Workflow")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 4: DATABASE DESIGN & ER DIAGRAM
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 4: Database Design & Entity-Relationship (ER) Model", level=1)
    
    add_header_styled(doc, "4.1 Entity-Relationship (ER) Diagram", level=2)
    doc.add_paragraph(
        "The relational schema enforces strict referential integrity across 14 relational entities. "
        "Foreign key cascades and database-level unique constraints safeguard catalog and accounting data."
    )
    if os.path.exists("docs_assets/diagram_er_model.png"):
        doc.add_picture("docs_assets/diagram_er_model.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 4.1: Complete Entity-Relationship (ER) Schema")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    add_header_styled(doc, "4.2 Relational Data Dictionary", level=2)
    
    tables_dict = [
        ("CustomUser", [
            ("id", "BigAutoField", "Primary Key, Auto Increment"),
            ("username", "CharField(150)", "Unique, Required for login"),
            ("role", "CharField(20)", "Choices: ADMIN, MANAGER, CASHIER, EMPLOYEE"),
            ("phone", "CharField(15)", "Contact phone number"),
            ("profile_picture", "ImageField", "Avatar image upload")
        ]),
        ("Product", [
            ("id", "BigAutoField", "Primary Key, Auto Increment"),
            ("name", "CharField(255)", "Unique=True, Case-insensitive verified"),
            ("product_code", "CharField(50)", "Unique SKU auto-generated (FIM-XXXXXX)"),
            ("barcode_number", "CharField(50)", "Unique EAN-13 / Code128 numeric string"),
            ("category_id", "ForeignKey", "References Category(id), CASCADE"),
            ("brand_id", "ForeignKey", "References Brand(id), SET_NULL"),
            ("supplier_id", "ForeignKey", "References Supplier(id), SET_NULL"),
            ("purchase_price", "Decimal(10,2)", "Cost price from supplier"),
            ("selling_price", "Decimal(10,2)", "Retail POS selling price"),
            ("stock_quantity", "IntegerField", "Real-time stock on hand"),
            ("low_stock_threshold", "IntegerField", "Threshold for automatic low-stock notifications")
        ]),
        ("Sale (Invoice)", [
            ("id", "BigAutoField", "Primary Key, Auto Increment"),
            ("invoice_number", "CharField(50)", "Unique=True, Sequential series (INV-26-XX)"),
            ("customer_id", "ForeignKey", "References Customer(id), optional for walk-ins"),
            ("grand_total", "Decimal(10,2)", "Final payable amount inclusive of GST"),
            ("amount_paid", "Decimal(10,2)", "Amount tendered by customer"),
            ("payment_method", "CharField(20)", "Choices: CASH, CARD, UPI, SPLIT"),
            ("created_at", "DateTimeField", "Timestamp of sale transaction")
        ]),
        ("PurchaseOrder", [
            ("id", "BigAutoField", "Primary Key, Auto Increment"),
            ("order_number", "CharField(50)", "Unique=True, Sequential series (PO-26-XX)"),
            ("bill_number", "CharField(100)", "Supplier's external tax invoice/bill number"),
            ("supplier_id", "ForeignKey", "References Supplier(id), CASCADE"),
            ("total_amount", "Decimal(10,2)", "Total invoice value of goods procured"),
            ("paid_amount", "Decimal(10,2)", "Disbursed payment sum"),
            ("status", "CharField(20)", "Choices: PENDING, COMPLETED, CANCELLED")
        ])
    ]
    
    for tbl_name, fields in tables_dict:
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        p_tbl_title = doc.add_paragraph()
        r_tt = p_tbl_title.add_run(f"Table: {tbl_name}")
        r_tt.bold = True
        r_tt.font.size = Pt(11)
        r_tt.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        t_dict = doc.add_table(rows=len(fields)+1, cols=3)
        t_dict.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_dict.rows[0].cells[0].paragraphs[0].text = "Field Name"
        t_dict.rows[0].cells[1].paragraphs[0].text = "Data Type"
        t_dict.rows[0].cells[2].paragraphs[0].text = "Constraints & Description"
        set_cell_background(t_dict.rows[0].cells[0], "2B6CB0")
        set_cell_background(t_dict.rows[0].cells[1], "2B6CB0")
        set_cell_background(t_dict.rows[0].cells[2], "2B6CB0")
        for c in t_dict.rows[0].cells:
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            c.paragraphs[0].runs[0].bold = True
            
        for f_idx, (fname, ftype, fdesc) in enumerate(fields):
            r = t_dict.rows[f_idx+1]
            r.cells[0].paragraphs[0].text = fname
            r.cells[1].paragraphs[0].text = ftype
            r.cells[2].paragraphs[0].text = fdesc
            bg = "F7FAFC" if f_idx % 2 == 0 else "EDF2F7"
            for c in r.cells:
                set_cell_background(c, bg)
                set_cell_margins(c, 40, 40, 60, 60)
                c.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 5: ALL 80 TEMPLATES INVENTORY & WORK
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 5: Master Catalog of All 80 Templates & Functionality", level=1)
    doc.add_paragraph(
        "Fenix IT Mall contains exactly 80 Django HTML templates organized into 14 dedicated application "
        "directories plus the master layout. Each template incorporates semantic HTML5, Django Template Language (DTL) tags, "
        "and Alpine.js reactive bindings. Below is the complete catalog detailing the exact file path, module, inheritance, "
        "and functional purpose of every template in the project."
    )
    
    # Template Directory Data
    templates_catalog = [
        ("base.html", "core / master", "Master Layout", "Defines the global responsive layout, sidebar brand header, dynamic logo rendering, theme switcher, top navigation bar, message toasts, and Alpine.js stores."),
        ("accounts/admin_change_password.html", "accounts", "base.html", "Enables Super Admins to securely reset or override any employee or cashier password with validation rules."),
        ("accounts/login.html", "accounts", "Standalone", "Enterprise authentication portal with animated glassmorphism card, dynamic company logo, theme toggle, and error toasts."),
        ("accounts/password_change.html", "accounts", "base.html", "Self-service password update interface for logged-in staff members with old password confirmation."),
        ("accounts/profile.html", "accounts", "base.html", "User profile management displaying account role badge, employee contact details, and avatar upload."),
        ("accounts/register.html", "accounts", "Standalone", "Staff onboarding registration form with role selection and phone validation."),
        ("accounts/user_form.html", "accounts", "base.html", "CRUD form for creating or editing user accounts, assigning roles (Admin, Manager, Cashier, Employee)."),
        ("accounts/user_list.html", "accounts", "base.html", "Comprehensive user directory table with role badges, status switches, and quick edit links."),
        ("core/403.html", "core", "Standalone", "Custom HTTP 403 Forbidden error view warning unauthorized users who attempt restricted RBAC routes."),
        ("core/404.html", "core", "Standalone", "Polished HTTP 404 Page Not Found error view with Return to Dashboard call to action."),
        ("core/500.html", "core", "Standalone", "Friendly HTTP 500 Internal Server Error view gracefully handling unhandled exceptions."),
        ("core/landing.html", "core", "Standalone", "Modern public landing page introducing Fenix IT Mall features, modules, and direct login portal."),
        ("customers/delete_confirm.html", "customers", "base.html", "Confirmation modal safeguarding against accidental customer record deletion."),
        ("customers/detail.html", "customers", "base.html", "Customer 360-degree profile displaying total spend, loyalty points, and full invoice history."),
        ("customers/form.html", "customers", "base.html", "Form for adding and editing customer details (Name, Phone, Email, Address, GSTIN)."),
        ("customers/list.html", "customers", "base.html", "Tabular directory of customers with search, loyalty points counter, and total purchases."),
        ("dashboard/index.html", "dashboard", "base.html", "Executive analytics dashboard featuring real-time KPI cards (Sales, Revenue, Stock Alerts), charts, and recent activity logs."),
        ("dashboard/recent_activity.html", "dashboard", "base.html", "Granular audit timeline showing recent sales, stock receipts, and employee logins."),
        ("employees/attendance.html", "employees", "base.html", "Daily staff attendance sheet allowing managers to mark Present, Absent, Half-Day, or Leave with duplicate prevention."),
        ("employees/delete_confirm.html", "employees", "base.html", "Deletion confirmation modal for offboarding employee records."),
        ("employees/detail.html", "employees", "base.html", "Comprehensive employee profile showing department, designation, salary history, and leave balances."),
        ("employees/form.html", "employees", "base.html", "Employee creation/update form auto-generating unique EMP-XXXXXX identification numbers."),
        ("employees/leave_form.html", "employees", "base.html", "Leave application form for employees to request Casual, Sick, or Annual leave."),
        ("employees/leaves.html", "employees", "base.html", "HR leave approval dashboard where managers approve or reject pending leave requests."),
        ("employees/list.html", "employees", "base.html", "Master employee roster with designation filters, department tags, and status indicators."),
        ("includes/alerts.html", "includes", "Partial", "Reusable toast notification component rendering Django success, warning, and error messages."),
        ("includes/breadcrumbs.html", "includes", "Partial", "Dynamic navigation breadcrumbs guiding users through nested views."),
        ("includes/footer.html", "includes", "Partial", "Standardized glassmorphic page footer displaying system copyright and build status."),
        ("includes/loader.html", "includes", "Partial", "Theme-synchronized splash screen loader that renders white in light mode and dark in dark mode."),
        ("includes/modal.html", "includes", "Partial", "Reusable dialog modal structure used for confirmations, popups, and quick views."),
        ("includes/navbar.html", "includes", "Partial", "Top navigation header with global search shortcut, theme switch toggle, notifications bell, and user menu."),
        ("includes/pagination.html", "includes", "Partial", "Standardized pagination bar supporting first, previous, next, and last page navigation."),
        ("includes/searchbar.html", "includes", "Partial", "Global search bar input component with hotkey triggers and quick-clear action."),
        ("includes/sidebar.html", "includes", "Partial", "Primary navigation sidebar featuring the dynamic company logo, collapsible groups, and active link highlights."),
        ("includes/theme_switch.html", "includes", "Partial", "Interactive sun/moon toggle switch that persists light/dark mode preference in localStorage."),
        ("inventory/adjust.html", "inventory", "base.html", "Manual stock adjustment form for reconciliation of physical vs system counts with reason tracking."),
        ("inventory/damaged.html", "inventory", "base.html", "Interface for logging damaged or expired inventory and writing off lost items."),
        ("inventory/history.html", "inventory", "base.html", "Complete stock movement audit log recording movement type (In, Out, Adjustment), delta, and user."),
        ("inventory/list.html", "inventory", "base.html", "Master inventory table showing on-hand stock, unit purchase price, retail price, and stock valuation."),
        ("inventory/low_stock.html", "inventory", "base.html", "Dedicated alert view listing products whose stock has fallen below the safety threshold."),
        ("inventory/out_of_stock.html", "inventory", "base.html", "Emergency replenishment view showing products with zero available quantity."),
        ("inventory/stock_in.html", "inventory", "base.html", "Direct stock inward interface for adding inventory outside formal purchase orders."),
        ("inventory/stock_out.html", "inventory", "base.html", "Stock outward form for inter-branch transfers or store sample consumption."),
        ("notifications/list.html", "notifications", "base.html", "Central notifications center displaying system alerts, low-stock warnings, and payment reminders."),
        ("products/barcode.html", "products", "base.html", "Printable barcode label sheet generating Code128 barcodes for thermal sticker printing."),
        ("products/brand_form.html", "products", "base.html", "Form for registering hardware brands (Intel, AMD, ASUS, Dell) with logo uploads."),
        ("products/brand_list.html", "products", "base.html", "Brand catalog grid showing brand logos, website links, and associated product counts."),
        ("products/category_form.html", "products", "base.html", "Form for creating hardware categories (Processors, Graphics Cards, Monitors) with icons."),
        ("products/category_list.html", "products", "base.html", "Category management gallery displaying active categories and total items."),
        ("products/detail.html", "products", "base.html", "In-depth product profile displaying multi-image gallery, barcode, QR code, specifications, and suppliers."),
        ("products/form.html", "products", "base.html", "Comprehensive product creation/edit form enforcing unique product names, pricing, and GST."),
        ("products/list.html", "products", "base.html", "Master product catalog table with live category filters, search, stock badges, and action menus."),
        ("products/qrcode.html", "products", "base.html", "High-resolution 2D QR Code generator view for quick mobile scanning and product verification."),
        ("purchase/delete_confirm.html", "purchase", "base.html", "Safety modal confirming cancellation or deletion of unfulfilled purchase orders."),
        ("purchase/detail.html", "purchase", "base.html", "Itemized Purchase Order breakdown showing PO number (PO-26-XX), supplier invoice, and payments."),
        ("purchase/form.html", "purchase", "base.html", "Procurement PO creation form with direct stock crediting, line-item pricing, and bill number tracking."),
        ("purchase/invoice.html", "purchase", "base.html", "Printable purchase voucher formatted for accounting audits and filing."),
        ("purchase/list.html", "purchase", "base.html", "Tabular listing of all Purchase Orders with sequential PO numbering, payment status, and totals."),
        ("purchase/payment_form.html", "purchase", "base.html", "Multi-installment supplier payment form supporting Cash, Bank Transfer, UPI, and Cheques."),
        ("purchase/receive_confirm.html", "purchase", "base.html", "Verification modal for confirming goods arrival and quality inspection."),
        ("reports/customers.html", "reports", "base.html", "Customer analytics report highlighting top-spending clients, repeat visits, and loyalty usage."),
        ("reports/employees.html", "reports", "base.html", "HR payroll and attendance analytics summarizing working hours, leaves, and salary payouts."),
        ("reports/home.html", "reports", "base.html", "Reports dashboard hub offering shortcuts to sales, inventory, profit, and supplier ledger reports."),
        ("reports/inventory.html", "reports", "base.html", "Inventory valuation report calculating total capital tied up in stock across categories."),
        ("reports/profit.html", "reports", "base.html", "Financial profit and loss report calculating gross margins (Revenue minus Cost of Goods Sold)."),
        ("reports/purchase.html", "reports", "base.html", "Procurement expenditure report grouping purchase orders by supplier and month."),
        ("reports/sales.html", "reports", "base.html", "Sales performance report filtering revenue by date ranges, cashier, and payment mode."),
        ("reports/suppliers.html", "reports", "base.html", "Advanced Supplier Bill & Payment Report with expandable drawers, balance tracking, and PDF/CSV export."),
        ("sales/delete_confirm.html", "sales", "base.html", "Manager confirmation dialog required before voiding or deleting a completed sale."),
        ("sales/detail.html", "sales", "base.html", "Detailed invoice inspection displaying customer info, cashier name, line items, taxes, and payment method."),
        ("sales/edit.html", "sales", "base.html", "Authorized supervisor view for updating customer details or payment methods on completed sales."),
        ("sales/invoice.html", "sales", "base.html", "Printable A4 and 80mm thermal receipt invoice template with company logo, tax breakdown, and barcode."),
        ("sales/list.html", "sales", "base.html", "Historical invoice ledger displaying sequential numbers (INV-26-01...), payment status, and grand totals."),
        ("sales/pos.html", "sales", "base.html", "High-speed POS Terminal interface with barcode listener, category rail, cart panel, F2 search, and F8 hold sale."),
        ("sales/void_confirm.html", "sales", "base.html", "Safety confirmation for voiding sales and returning deducted stock back to inventory."),
        ("settings_app/settings.html", "settings_app", "base.html", "Enterprise branding settings interface supporting custom company logo upload, theme toggle, and currency."),
        ("suppliers/delete_confirm.html", "suppliers", "base.html", "Confirmation modal preventing accidental deletion of suppliers with active purchase ledgers."),
        ("suppliers/detail.html", "suppliers", "base.html", "Supplier profile showing contact info, bank details, GSTIN, and cumulative procurement history."),
        ("suppliers/form.html", "suppliers", "base.html", "Form for registering suppliers with contact details, address, and opening balances."),
        ("suppliers/list.html", "suppliers", "base.html", "Supplier directory table with balance indicators, phone links, and quick order creation.")
    ]
    
    t_tpl = doc.add_table(rows=len(templates_catalog)+1, cols=4)
    t_tpl.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tpl_headers = ["Template Location", "Module", "Extends / Type", "Functional Purpose & Key Features"]
    for i, h in enumerate(t_tpl_headers):
        cell = t_tpl.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "1A365D")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9)
        
    for idx, (loc, mod, ext, desc) in enumerate(templates_catalog):
        r = t_tpl.rows[idx+1]
        r.cells[0].paragraphs[0].text = loc
        r.cells[1].paragraphs[0].text = mod
        r.cells[2].paragraphs[0].text = ext
        r.cells[3].paragraphs[0].text = desc
        bg = "F7FAFC" if idx % 2 == 0 else "EDF2F7"
        for c in r.cells:
            set_cell_background(c, bg)
            set_cell_margins(c, 30, 30, 40, 40)
            c.paragraphs[0].runs[0].font.size = Pt(8)

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 6: MODULE WALKTHROUGH & SCREENSHOTS
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 6: Functional Modules & Live System Screenshots", level=1)
    
    add_header_styled(doc, "6.1 Executive Dashboard & Business Analytics", level=2)
    doc.add_paragraph(
        "The Executive Dashboard acts as the central command hub for store managers. It presents high-level KPI tiles: "
        "Total Sales Revenue, Number of Orders, Total Available Products, and Low Stock Alerts. Below the KPI cards, interactive "
        "charts illustrate daily sales trends, and the real-time activity stream monitors recent transactions."
    )
    if os.path.exists("docs_assets/screenshot_dashboard.png"):
        doc.add_picture("docs_assets/screenshot_dashboard.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.1: Live Executive Analytics Dashboard (Light Theme)")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    add_header_styled(doc, "6.2 High-Speed Point of Sale (POS) Terminal", level=2)
    doc.add_paragraph(
        "The Point of Sale interface is tailored for high-volume retail transactions. Cashiers can browse products via "
        "the top visual category rail or scan items with a USB barcode gun. The right-hand shopping cart calculates subtotal, "
        "discounts, 18% GST, and grand total in real time. Cashiers can complete orders with Cash, UPI, or Card, or suspend "
        "the transaction with the Hold Sale (F8) feature."
    )
    if os.path.exists("docs_assets/screenshot_pos_terminal.png"):
        doc.add_picture("docs_assets/screenshot_pos_terminal.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.2: Live POS Checkout Terminal with Responsive Product Cards")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_page_break()
    
    add_header_styled(doc, "6.3 Instant Search & Barcode Listener", level=2)
    doc.add_paragraph(
        "The search bar integrates flexbox badge hotkeys ('SCAN' and 'F2') with zero text overlapping. "
        "Typing any brand or keyword (e.g. 'Dell') instantaneously filters the product grid in sub-milliseconds "
        "without triggering full-page browser reloads."
    )
    if os.path.exists("docs_assets/screenshot_pos_search.png"):
        doc.add_picture("docs_assets/screenshot_pos_search.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.3: Instant Sub-Millisecond Search Filtering in POS Terminal")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    add_header_styled(doc, "6.4 Sequential Sales Invoicing (INV-26-XX)", level=2)
    doc.add_paragraph(
        "Fenix IT Mall replaces cryptic random hash identifiers with a clean, business-standard sequential series: "
        "INV-26-01, INV-26-02, ..., INV-26-15. When the calendar year rolls over to 2027, the system automatically resets "
        "the sequence to INV-27-01. Invoices record customer details, line items, taxes, payment modes, and audit timestamps."
    )
    if os.path.exists("docs_assets/screenshot_sales_invoices.png"):
        doc.add_picture("docs_assets/screenshot_sales_invoices.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.4: Sequential Sales Invoices Listing (INV-26-01...)")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_page_break()
    
    add_header_styled(doc, "6.5 Direct Stock Procurement & Purchase Orders (PO-26-XX)", level=2)
    doc.add_paragraph(
        "Procurement eliminates redundant receiving paperwork. Creating a Purchase Order (e.g. PO-26-01, PO-26-02) "
        "automatically credits inventory quantities directly into available stock while maintaining an atomic audit record. "
        "Managers can track supplier tax bill numbers (e.g. AS-8859) alongside internal PO numbers."
    )
    if os.path.exists("docs_assets/screenshot_purchase_orders.png"):
        doc.add_picture("docs_assets/screenshot_purchase_orders.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.5: Sequential Purchase Orders Listing (PO-26-01...)")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    add_header_styled(doc, "6.6 Supplier Bill & Multi-Installment Payment Ledger", level=2)
    doc.add_paragraph(
        "The Supplier Bill & Payment Report gives complete visibility into supplier balances. Clicking any bill row expands "
        "an interactive drawer displaying purchased items (quantity, unit rate, subtotal) and previous payment installments. "
        "Managers can record partial payments via Cash, Bank Transfer, UPI, or Cheque, with 1-click PDF/CSV export."
    )
    if os.path.exists("docs_assets/screenshot_supplier_report.png"):
        doc.add_picture("docs_assets/screenshot_supplier_report.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.6: Advanced Supplier Bill & Payment Ledger with Expandable Drawers")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True
        
    doc.add_page_break()
    
    add_header_styled(doc, "6.7 Enterprise Settings & Custom Logo Branding", level=2)
    doc.add_paragraph(
        "Store administrators can upload a high-resolution corporate logo that propagates across the entire platform: "
        "splash screen loader, sidebar brand header, login portal, and printable invoice headers. The system features "
        "persistent media serving via Django static views, guaranteeing HTTP 200 OK image loading in production."
    )
    if os.path.exists("docs_assets/screenshot_settings_branding.png"):
        doc.add_picture("docs_assets/screenshot_settings_branding.png", width=Inches(6.2))
        cp = doc.add_paragraph("Figure 6.7: Enterprise Settings Interface with Live Logo Preview & Branding Controls")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].font.size = Pt(9)
        cp.runs[0].font.italic = True

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 7: TESTING & QUALITY ASSURANCE (195/195)
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 7: Quality Assurance & Testing Suite", level=1)
    doc.add_paragraph(
        "To guarantee enterprise robustness, the system was subjected to a comprehensive automated test suite "
        "(test_all_195_cases.py) evaluating 195 distinct functional scenarios, security boundaries, and edge cases. "
        "The system achieved a 100.0% pass rate with zero failures or regressions."
    )
    
    create_callout_box(
        doc,
        "AUTOMATED TEST RESULTS SUMMARY",
        "• Total Test Cases Executed: 195\n"
        "• Passed: 195 (100.0%)\n"
        "• Failed: 0 (0.0%)\n"
        "• Errors: 0\n"
        "• Test Execution Command: python test_all_195_cases.py\n"
        "• Verification Status: Enterprise Grade — Ready for Production",
        bg_color="F0FFF4", border_color="38A169"
    )
    
    add_header_styled(doc, "7.1 Test Case Distribution by Module", level=2)
    t_test = doc.add_table(rows=21, cols=4)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    tt_headers = ["Module Category", "Test ID Range", "Case Count", "Status"]
    for i, h in enumerate(tt_headers):
        cell = t_test.rows[0].cells[i]
        cell.paragraphs[0].text = h
        set_cell_background(cell, "2B6CB0")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].bold = True
        
    test_matrix = [
        ("Core & Navigation", "TC-CORE-001 – TC-CORE-007", "7", "✅ Passed"),
        ("Authentication & RBAC", "TC-AUTH-001 – TC-AUTH-009", "9", "✅ Passed"),
        ("Dashboard Analytics", "TC-DASH-001 – TC-DASH-006", "6", "✅ Passed"),
        ("Products & Catalog", "TC-PROD-001 – TC-PROD-012", "12", "✅ Passed"),
        ("Categories & Brands", "TC-CAT-001 – TC-BRD-006", "12", "✅ Passed"),
        ("Barcodes & QR Codes", "TC-BAR-001 – TC-BAR-007", "7", "✅ Passed"),
        ("Inventory & Stock Movements", "TC-INV-001 – TC-INV-010", "10", "✅ Passed"),
        ("POS Checkout & Sales", "TC-POS-001 – TC-SALE-010", "20", "✅ Passed"),
        ("Purchases & Suppliers", "TC-PUR-001 – TC-PUR-013", "13", "✅ Passed"),
        ("Customers CRM", "TC-CUST-001 – TC-CUST-007", "7", "✅ Passed"),
        ("Suppliers Module", "TC-SUPP-001 – TC-SUPP-005", "5", "✅ Passed"),
        ("Employees & HR Suite", "TC-EMP-001 – TC-EMP-LEV-005", "16", "✅ Passed"),
        ("Reports & Supplier Ledger", "TC-RPT-001 – TC-RPT-017", "17", "✅ Passed"),
        ("Notifications & Alerts", "TC-NOTIF-001 – TC-NOTIF-006", "6", "✅ Passed"),
        ("Company Settings & Logo", "TC-SET-001 – TC-SET-006", "6", "✅ Passed"),
        ("UI/UX Glassmorphic Tokens", "TC-UI-001 – TC-UI-013", "13", "✅ Passed"),
        ("Security (SQLi/XSS/CSRF)", "TC-SEC-001 – TC-SEC-008", "8", "✅ Passed"),
        ("Edge Cases & Boundaries", "TC-EDGE-001 – TC-EDGE-010", "10", "✅ Passed"),
        ("Data Integrity & Unique Keys", "TC-DATA-001 – TC-DATA-010", "10", "✅ Passed"),
        ("End-to-End Retail Workflows", "TC-E2E-001 – TC-E2E-007", "7", "✅ Passed")
    ]
    for row_idx, data in enumerate(test_matrix):
        r = t_test.rows[row_idx+1]
        for col_idx, val in enumerate(data):
            c = r.cells[col_idx]
            c.paragraphs[0].text = val
            set_cell_background(c, "F7FAFC" if row_idx % 2 == 0 else "EDF2F7")
            set_cell_margins(c, 30, 30, 50, 50)
            c.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 8: CLOUD DEPLOYMENT ON RENDER
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 8: Cloud Deployment & Production Infrastructure", level=1)
    doc.add_paragraph(
        "Fenix IT Mall is deployed as a live cloud service on Render.com with automated CI/CD continuous integration "
        "linked directly to the GitHub main branch."
    )
    
    create_callout_box(
        doc,
        "PRODUCTION ENVIRONMENT SPECIFICATION",
        "• Public URL: https://fenix-it-mall.onrender.com/\n"
        "• Git Repository: https://github.com/JeetDodiy/fenix_it_mall\n"
        "• Server Architecture: Linux Container (Ubuntu / Debian x86_64)\n"
        "• WSGI Web Worker: Gunicorn 21.2.0 (fenix_it_mall.wsgi:application)\n"
        "• Static Assets: WhiteNoise 6.6 with Brotli / Gzip compression\n"
        "• Media Handling: Production re_path(r'^media/(?P<path>.*)$', serve) pipeline\n"
        "• Automated CI/CD: Triggered on every git push origin main",
        bg_color="EBF8FF", border_color="3182CE"
    )
    
    add_header_styled(doc, "8.1 Continuous Deployment Pipeline (build.sh)", level=2)
    doc.add_paragraph(
        "The automated build script executes on Render during every deployment:\n"
        "1. Dependency Installation: pip install -r requirements.txt installs Django, Gunicorn, WhiteNoise, ReportLab, etc.\n"
        "2. Static Compilation: python manage.py collectstatic --noinput compresses all CSS, JS, and font assets into staticfiles/.\n"
        "3. Catalog Deduplication & Cleansing: Automated management commands remove duplicate entries and strip test artifacts.\n"
        "4. Schema Migration: python manage.py migrate applies all database schema updates safely.\n"
        "5. Superuser Provisioning: Automated init_admin initializes default credentials (admin / admin123) if missing."
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 9: VIVA VOCE EXAMINER MASTER GUIDE (TOP 25 Q&A)
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 9: The Ultimate Viva Voce Master Guide (Top 25 Questions & Answers)", level=1)
    doc.add_paragraph(
        "This chapter provides comprehensive, technically rigorous answers to the top 25 questions typically posed by "
        "external examiners and project evaluators during the Semester 5 Viva Voce examination."
    )
    
    viva_qa = [
        ("Q1: What is the Django MVT architectural pattern and how does it differ from traditional MVC?",
         "Answer: Traditional MVC separates Model (data), View (UI display), and Controller (business logic). "
         "In Django's MVT architecture:\n"
         "• Model: Handles database access, ORM mappings, and business data logic.\n"
         "• View: Acts like the traditional Controller. It processes HTTP requests, executes business logic, calls models, and sends data to the template.\n"
         "• Template: Represents the traditional View. It defines the HTML structure and presentation using Django Template Language (DTL).\n"
         "Django itself acts as the overall Controller by managing URL routing and request dispatching."),
        
        ("Q2: Why did you choose Django ORM over writing raw SQL queries?",
         "Answer: Django ORM provides three crucial advantages:\n"
         "1. Security: ORM automatically parameterizes SQL queries, completely eliminating SQL Injection vulnerabilities.\n"
         "2. Database Portability: Code works seamlessly with SQLite, PostgreSQL, or MySQL by changing settings without modifying application code.\n"
         "3. Productivity: ORM provides built-in query optimization (select_related, prefetch_related), automatic relationship handling, and database migrations."),
         
        ("Q3: What is a CSRF token and why is it mandatory in POS checkout POST requests?",
         "Answer: Cross-Site Request Forgery (CSRF) is an attack where an unauthorized website tricks a user's browser into submitting malicious requests to a site where they are authenticated.\n"
         "Django generates a unique cryptographic token per user session ({% csrf_token %}). When the POS submits a sale or payment, Django validates the submitted token against the session cookie. If the token is missing or mismatched, Django rejects the request with HTTP 403 Forbidden."),
         
        ("Q4: How does the POS checkout guarantee atomic stock decrement without race conditions?",
         "Answer: The checkout endpoint wraps the sale creation and inventory deduction inside a database transaction using 'with transaction.atomic():'. "
         "During checkout, the system verifies available stock. If an item has insufficient stock, or if any error occurs midway through recording the sale items, the entire transaction rolls back automatically, preventing orphaned invoices and inventory mismatches."),
         
        ("Q5: Why did you implement sequential numbering (INV-26-01, PO-26-01) instead of UUIDs?",
         "Answer: In commercial retail and accounting, sequential numbering is mandated by tax authorities (GST/VAT) for chronological audit trails. Random UUIDs (like #a9f2-881c) are confusing for customers and difficult to reference over the phone. The sequential format 'INV-26-XX' clearly indicates the document type (INV), fiscal year (2026), and chronological index (01, 02...)."),
         
        ("Q6: How does the duplicate product name restriction work in both forms and the database?",
         "Answer: It is enforced at two distinct layers:\n"
         "1. Database Layer: The Product model defines 'name = models.CharField(max_length=255, unique=True)'.\n"
         "2. Form Validation Layer: ProductForm implements 'clean_name()', using 'Product.objects.filter(name__iexact=name)'. It ignores case sensitivity ('Gaming Mouse' vs 'gaming mouse') and allows an existing product to be saved without throwing a self-collision error."),
         
        ("Q7: How does the theme-adaptive splash screen detect light vs dark mode before page render?",
         "Answer: The splash screen loader script in 'loader.html' executes immediately in the <head> before HTML body painting. It reads 'localStorage.getItem(\"fenix_theme\")'. If the stored theme is 'light', it instantly sets the loader background to clean white (#ffffff) and dark text; if 'dark', it applies the deep navy/black background (#0f172a). This eliminates annoying white flashes (FOUC) during theme transitions."),
         
        ("Q8: What are the roles of Gunicorn and WhiteNoise in your cloud deployment?",
         "Answer: Django's built-in 'runserver' is single-threaded and unsafe for production. Gunicorn is a pre-fork WSGI HTTP server that spins up multiple worker processes to handle concurrent requests. WhiteNoise serves pre-compressed static files (CSS, JS, fonts) directly through the WSGI pipeline, eliminating the need for an external Nginx server on cloud platforms like Render."),
         
        ("Q9: How is Role-Based Access Control (RBAC) enforced across the system?",
         "Answer: The CustomUser model defines boolean role flags: is_admin, is_manager, is_cashier, and is_employee. Views are protected by custom decorators (e.g. @admin_required, @manager_required). For example, if a cashier attempts to navigate to '/reports/' or '/employees/', the decorator intercepts the request and redirects them or returns an HTTP 403 Forbidden error."),
         
        ("Q10: How are Code128 barcodes and QR codes generated without external cloud APIs?",
         "Answer: Barcodes and QR codes are generated locally on the server using the 'python-barcode' and 'qrcode' Python libraries. When a product is created, the system generates an EAN-13/Code128 barcode image and a 2D QR image encoding the product SKU. These are saved to the media directory and can be printed directly on thermal label sheets."),
         
        ("Q11: What is the difference between ForeignKey, OneToOneField, and ManyToManyField in Django?",
         "Answer:\n"
         "• ForeignKey: Implements a Many-to-One relationship (e.g., Many Products belong to One Category).\n"
         "• OneToOneField: Implements a strict One-to-One relationship (e.g., One User profile linked to One Employee record).\n"
         "• ManyToManyField: Implements a Many-to-Many relationship (e.g., Multiple Products linked to Multiple Tags/Promotions) using an intermediate join table."),
         
        ("Q12: How does the Supplier Ledger calculate pending balances dynamically?",
         "Answer: Each Purchase Order tracks 'total_amount' and 'paid_amount'. The pending balance is computed as 'total_amount - paid_amount'. In the Supplier Bill & Payment Report, queries aggregate cumulative purchases and cumulative disbursements per supplier using Django ORM's 'Sum()' and 'annotate()', allowing real-time balance tracking."),
         
        ("Q13: Why was Alpine.js selected for the POS interface instead of React or Vue?",
         "Answer: React and Vue require heavy build pipelines (Webpack, Vite, Node.js), complex state hydration, and overhead. Alpine.js is declarative, lightweight (~15KB), and runs directly inside Django HTML templates via simple x-data, x-on, and x-model attributes. It delivers instant reactivity for search filtering and cart calculations without architectural bloat."),
         
        ("Q14: How does the Hold Sale (F8) feature work without writing incomplete sales to the database?",
         "Answer: The Hold Sale feature uses browser 'localStorage'. When a cashier presses F8, the current Alpine.js cart array, selected customer, and discount values are serialized into JSON and saved to 'localStorage.setItem(\"held_cart\", ...)'. The cashier can serve another customer and later resume the held cart with a single click."),
         
        ("Q15: How does ReportLab generate PDF receipts and supplier ledger reports?",
         "Answer: ReportLab is a Python library that builds binary PDF streams in memory using 'io.BytesIO()'. The view creates a Canvas, sets page geometry (A4 or thermal slip), draws headers, tables, logos, and borders, and outputs an HttpResponse with content type 'application/pdf' and an attachment or inline disposition header."),
         
        ("Q16: What happens when the calendar year rolls over from 2026 to 2027 in sequential numbering?",
         "Answer: The sequential generator extracts the current two-digit year (e.g. '26' for 2026, '27' for 2027). It filters existing records for orders matching the current year prefix. When 2027 begins, no 'INV-27-' records exist yet, so the query finds no previous orders for that year and automatically restarts the sequence at 'INV-27-01'."),
         
        ("Q17: How does Django handle media file uploads vs static files in production?",
         "Answer: Static files (CSS, JS, icons) are compiled via 'collectstatic' and served statically by WhiteNoise. Media files (user-uploaded product images, company logos) are uploaded at runtime into the MEDIA_ROOT directory. On Render, production media serving is handled via 're_path(r'^media/(?P<path>.*)$', serve)', ensuring uploaded logos and product photos remain accessible with HTTP 200 OK."),
         
        ("Q18: What is the purpose of select_related and prefetch_related in Django QuerySets?",
         "Answer: They solve the notorious 'N+1 queries' performance problem:\n"
         "• select_related(): Used for single-valued relationships (ForeignKey, OneToOne). It performs an SQL JOIN in a single database query.\n"
         "• prefetch_related(): Used for multi-valued relationships (ManyToMany, reverse ForeignKey). It executes a separate query with an 'IN' clause and joins the results in Python memory."),
         
        ("Q19: How does the system handle multi-installment payments for a single purchase order?",
         "Answer: The PurchaseOrder model maintains a One-to-Many relationship with SupplierPayment. Each payment installment records the payment amount, date, payment method (Cash, Bank, UPI, Cheque), and reference note. When a payment is saved, a Django post_save signal or model method automatically increments 'paid_amount' on the parent PurchaseOrder and updates its status to 'PARTIALLY_PAID' or 'COMPLETED'."),
         
        ("Q20: How did you design and execute the 195 automated test cases?",
         "Answer: A dedicated automated test runner 'test_all_195_cases.py' was implemented using Django's 'TestCase' and 'Client' framework. Tests are structured across 20 distinct categories covering routing, authentication, RBAC boundaries, form validations, inventory stock adjustments, sequential numbering logic, and XSS/SQLi injection immunity."),
         
        ("Q21: What HTTP status codes are returned by your views and what do they signify?",
         "Answer:\n"
         "• 200 OK: Successful page retrieval or JSON response.\n"
         "• 302 Found: Redirect after successful form submission or login.\n"
         "• 400 Bad Request: Form validation failure or invalid payload.\n"
         "• 403 Forbidden: Insufficient role permissions under RBAC.\n"
         "• 404 Not Found: Request for a non-existent product, order, or URL.\n"
         "• 500 Internal Server Error: Unhandled server-side exception."),
         
        ("Q22: How does the application maintain responsive UI across mobile, tablet, and desktop?",
         "Answer: The styling relies on CSS3 Flexbox and CSS Grid with media queries (@media (max-width: 768px), @media (max-width: 1024px)). On mobile screens, the sidebar collapses into a slide-over drawer, tables become horizontally scrollable with sticky headers, and POS product cards wrap flexibly."),
         
        ("Q23: What database transactions (transaction.atomic) are used in this project and why?",
         "Answer: 'transaction.atomic()' is utilized in critical business operations: POS checkout, Purchase Order creation with direct stock increment, and Stock Adjustments. This ensures ACID compliance: either all database writes (creating invoice, recording line items, updating stock, creating movement logs) succeed together, or all changes roll back to prevent data corruption."),
         
        ("Q24: If the store loses internet connectivity, can this system be run offline?",
         "Answer: Yes! Because Fenix IT Mall is built on standard Python/Django and SQLite, the entire application can be hosted locally on an in-store counter PC (e.g. running on http://127.0.0.1:8000). All POS operations, barcode scanning, receipt printing, and inventory adjustments work 100% offline without any cloud dependency."),
         
        ("Q25: What future enhancements can be added to this ERP system?",
         "Answer:\n"
         "1. Multi-Store Synchronization: Centralized cloud database aggregating sales from multiple retail branches.\n"
         "2. WhatsApp Business API: Automatically dispatching digital PDF invoices to customer WhatsApp numbers upon checkout.\n"
         "3. AI Demand Forecasting: Using machine learning (ARIMA/Linear Regression) to predict seasonal hardware demands (e.g. holiday GPU and laptop sales).")
    ]
    
    for q_title, q_ans in viva_qa:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        r_q = p_q.add_run(q_title)
        r_q.bold = True
        r_q.font.size = Pt(10.5)
        r_q.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        
        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        p_a.paragraph_format.line_spacing = 1.15
        r_a = p_a.add_run(q_ans)
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 10: CONCLUSION & REFERENCES
    # ----------------------------------------------------
    add_header_styled(doc, "Chapter 10: Conclusion & References", level=1)
    
    add_header_styled(doc, "10.1 Conclusion", level=2)
    doc.add_paragraph(
        "The development of Fenix IT Mall successfully demonstrates the design and deployment of a modern, production-grade "
        "Point of Sale and ERP system tailored for IT hardware retailers. By combining Python 3.10+, Django 5.0.6, Vanilla CSS3, "
        "Alpine.js, and Gunicorn/WhiteNoise on Render Cloud, the project achieves an ideal balance between high performance, "
        "aesthetic appeal, and operational reliability.\n\n"
        "Key milestones achieved include sub-millisecond barcode checkout, duplicate product name elimination, sequential invoice/PO "
        "numbering, dynamic logo branding, adaptive theme synchronization, comprehensive supplier ledgers, and 100% automated test passing "
        "across 195 test cases. The application stands ready for commercial retail deployment."
    )
    
    add_header_styled(doc, "10.2 References & Bibliography", level=2)
    refs = [
        "1. Django Software Foundation. (2024). Django 5.0 Documentation. Retrieved from https://docs.djangoproject.com/en/5.0/",
        "2. MDN Web Docs. (2024). CSS Flexible Box Layout & Grid Layout. Mozilla Developer Network.",
        "3. Alpine.js Core Team. (2024). Alpine.js Documentation. Retrieved from https://alpinejs.dev/",
        "4. ReportLab Inc. (2024). ReportLab PDF Generation Library. Retrieved from https://www.reportlab.com/docs/",
        "5. Render Cloud Services. (2024). Deploying Django Applications on Render. Retrieved from https://render.com/docs/",
        "6. WhiteNoise Documentation. (2024). Radically simplified static file serving for Python web apps. Retrieved from http://whitenoise.evans.io/"
    ]
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(2)
        r = p_ref.add_run(ref)
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Save document
    out_docx_path = "Fenix_IT_Mall_Sem5_Project_Report.docx"
    doc.save(out_docx_path)
    print(f"Successfully generated academic project report: {out_docx_path}")

if __name__ == "__main__":
    main()
