import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts
try:
    pdfmetrics.registerFont(TTFont('TimesNewRoman', r'C:\Windows\Fonts\times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', r'C:\Windows\Fonts\timesbd.ttf'))
    FONT_NORMAL = 'TimesNewRoman'
    FONT_BOLD = 'TimesNewRoman-Bold'
except Exception:
    FONT_NORMAL = 'Times-Roman'
    FONT_BOLD = 'Times-Bold'

# Register Segoe UI Symbol for exact matching bullets ➢ and ❖
pdfmetrics.registerFont(TTFont('SegoeUISymbol', r'C:\Windows\Fonts\seguisym.ttf'))

ARROW_BULLET = '<font name="SegoeUISymbol" size="13">&#x27a2;</font> '
DIAMOND_BULLET = '<font name="SegoeUISymbol" size="13">&#x2756;</font> '

PAGE_WIDTH, PAGE_HEIGHT = A4

def draw_decorations(canvas_obj, doc):
    canvas_obj.saveState()
    
    # 1. Double Black Border
    # Outer rectangle: 2.2pt width
    canvas_obj.setStrokeColor(colors.black)
    canvas_obj.setLineWidth(2.2)
    canvas_obj.rect(22, 22, PAGE_WIDTH - 44, PAGE_HEIGHT - 44)
    
    # Inner rectangle: 0.75pt width
    canvas_obj.setLineWidth(0.75)
    canvas_obj.rect(26, 26, PAGE_WIDTH - 52, PAGE_HEIGHT - 52)
    
    # 2. Top-Left Header: "Fenix IT Mall" (on all pages)
    canvas_obj.setFont(FONT_NORMAL, 10.5)
    canvas_obj.setFillColor(colors.black)
    canvas_obj.drawString(44, PAGE_HEIGHT - 42, "Fenix IT Mall")
    
    # 3. Bottom-Center Page Number (Pages 4 through 36 -> numbered 1 to 33)
    pno = canvas_obj._pageNumber
    if pno >= 4:
        display_num = str(pno - 3)
        canvas_obj.setFont(FONT_NORMAL, 10.5)
        canvas_obj.drawCentredString(PAGE_WIDTH / 2.0, 36, display_num)
        
    canvas_obj.restoreState()

def create_image_flowable(img_path, max_w=490, max_h=265):
    if not os.path.exists(img_path):
        return Paragraph(f"[Image Missing: {img_path}]", ParagraphStyle('err', fontName=FONT_NORMAL, fontSize=10))
    with PILImage.open(img_path) as im:
        orig_w, orig_h = im.size
    
    scale = min(max_w / orig_w, max_h / orig_h)
    w = orig_w * scale
    h = orig_h * scale
    return RLImage(img_path, width=w, height=h)

def build_pdf():
    pdf_path = "Fenix_IT_Mall_Project_Report.pdf"
    print(f"Building {pdf_path} (Matching Brijesh_Msit_Sem_4.pdf)...")

    # Document margins: left=44, right=44, top=50, bottom=50
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=44,
        rightMargin=44,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Typography styles matching Brijesh's report
    style_cover_label = ParagraphStyle('CoverLabel', fontName=FONT_BOLD, fontSize=13, leading=17, alignment=TA_CENTER, textColor=colors.black)
    style_cover_title = ParagraphStyle('CoverTitle', fontName=FONT_BOLD, fontSize=24, leading=28, alignment=TA_CENTER, textColor=colors.HexColor('#4A90E2'))
    style_cover_sub = ParagraphStyle('CoverSub', fontName=FONT_NORMAL, fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.black)
    style_cover_guide = ParagraphStyle('CoverGuide', fontName=FONT_BOLD, fontSize=12.5, leading=16, alignment=TA_CENTER, textColor=colors.HexColor('#4A90E2'))
    style_cover_prep = ParagraphStyle('CoverPrep', fontName=FONT_BOLD, fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.HexColor('#4A90E2'))

    # Underlined Centered Heading for sections
    style_h1_underlined = ParagraphStyle('H1U', fontName=FONT_BOLD, fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.black, spaceAfter=14)
    style_screen_main_title = ParagraphStyle('ScrMainH', fontName=FONT_BOLD, fontSize=18, leading=22, alignment=TA_CENTER, textColor=colors.black, spaceAfter=8)
    style_screen_sub_title = ParagraphStyle('ScrSubH', fontName=FONT_BOLD, fontSize=14, leading=18, alignment=TA_LEFT, textColor=colors.black, spaceAfter=8)

    style_prof_bullet = ParagraphStyle('ProfB', fontName=FONT_NORMAL, fontSize=12, leading=20, alignment=TA_LEFT, textColor=colors.black, spaceAfter=13)
    style_req_bullet = ParagraphStyle('ReqB', fontName=FONT_NORMAL, fontSize=12.5, leading=22, alignment=TA_LEFT, textColor=colors.black, spaceAfter=22)
    style_scr_bullet = ParagraphStyle('ScrB', fontName=FONT_NORMAL, fontSize=11.5, leading=17, alignment=TA_LEFT, textColor=colors.black, spaceAfter=7)

    story = []

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("A PROJECT REPORT ON", style_cover_label))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Fenix IT Mall", style_cover_title))
    story.append(Spacer(1, 24))
    story.append(Paragraph("SUBMITTED TO:", style_cover_label))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Geetanjali College of Computer Science and Commerce (BBA) Saurashtra University Rajkot", ParagraphStyle('inst', fontName=FONT_BOLD, fontSize=12.5, leading=17, alignment=TA_CENTER)))
    story.append(Spacer(1, 24))
    story.append(Paragraph("FRONT END :", style_cover_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("HTML5, Vanilla CSS3, Alpine.js", style_cover_sub))
    story.append(Spacer(1, 14))
    story.append(Paragraph("BACK END :", style_cover_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Python 3.10+, Django 5.0", style_cover_sub))
    story.append(Spacer(1, 16))
    story.append(Paragraph("AFFILIATED BY :", style_cover_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Saurashtra University", style_cover_sub))
    story.append(Spacer(1, 16))
    story.append(Paragraph("ACADEMIC YEAR :", style_cover_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("2025-2026", style_cover_sub))
    story.append(Spacer(1, 16))
    story.append(Paragraph("PROJECT GUIDE:", style_cover_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Prof. Harsh Joshi", style_cover_guide))
    story.append(Spacer(1, 18))
    story.append(Paragraph("PREPARED BY:", style_cover_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Jeet Dodiya", style_cover_prep))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Acknowledgement</u>", style_h1_underlined))
    story.append(Spacer(1, 15))
    
    ack_texts = [
        "First and foremost, we are sincerely thankful to Saurashtra University for giving us the opportunity to work on this project as part of our curriculum.",
        "We extend our gratitude to Geetanjali Group Of Colleges for providing us with the resources and environment needed to develop our project.",
        "We are particularly grateful to our Head of Department, Prof. Brijesh Shah for their constant support and guidance throughout the project.",
        "We would like to express our deepest appreciation to our project guide, prof. Kishorsinh Vala, who guided us through the analysis and development phases of our project, providing invaluable advice and support.",
        "We are also thankful to all well-wishers and friends who supported us during the project development."
    ]
    for txt in ack_texts:
        story.append(Paragraph(f"• {txt}", ParagraphStyle('ack_b', fontName=FONT_NORMAL, fontSize=11.5, leading=18, spaceAfter=14)))
        
    story.append(Spacer(1, 35))
    story.append(Paragraph("Yours Faithfully,<br/><br/><b>Jeet Dodiya</b>", ParagraphStyle('yf', fontName=FONT_NORMAL, fontSize=11.5, leading=17, alignment=TA_LEFT, leftIndent=25)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: INDEX
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Index</u>", style_h1_underlined))
    story.append(Spacer(1, 15))

    index_data = [
        ["SR.NO", "TOPICNAME", "PAGENO."],
        ["1", "Project Profile", "1"],
        ["2", "Project Requirement", "2"],
        ["3", "Technology Requirement", "3"],
        ["4", "Data Flow Diagram", "4"],
        ["5", "E-R Diagram", "6"],
        ["6", "SDLC", "7"],
        ["7", "Data Dictionary", "8"],
        ["8", "Test cases", "10"],
        ["9", "Screenshots", "11"],
        ["10", "Future Enhancement of project", "32"],
        ["11", "Webliography", "33"],
    ]
    
    t_index = Table(index_data, colWidths=[70, 340, 70])
    t_index.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NORMAL),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_index)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4 (Page No. 1): PROJECT PROFILE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Project Profile</u>", style_h1_underlined))
    story.append(Spacer(1, 18))

    profile_items = [
        ("Project Title", "Fenix IT Mall"),
        ("Development Software", "Visual Studio Code"),
        ("Front End", "HTML5, Vanilla CSS3, Alpine.js"),
        ("Back End", "Python 3.10+, Django 5.0.6"),
        ("Academic Year", "2025-2026"),
        ("Developed By", "Jeet Dodiya"),
        ("Submitted To", "Geetanjali College of Computer Science and Commerce (BBA) Saurashtra University Rajkot"),
        ("Documentation Tool", "Microsoft Word"),
        ("Operating System", "Windows 11")
    ]
    for lbl, val in profile_items:
        story.append(Paragraph(f"{ARROW_BULLET} <b>{lbl}:</b> {val}", style_prof_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5 (Page No. 2): PROJECT REQUIREMENT
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Project Requirement</u>", style_h1_underlined))
    story.append(Spacer(1, 24))

    reqs = [
        ("Processor", "Intel Core i3 or higher"),
        ("RAM", "4 GB or more"),
        ("Hard Disk", "500 GB or more")
    ]
    for lbl, val in reqs:
        story.append(Paragraph(f"{DIAMOND_BULLET} <b>{lbl}:</b> {val}", style_req_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6 (Page No. 3): TECHNOLOGY REQUIREMENT
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Technology Requirement</u>", style_h1_underlined))
    story.append(Spacer(1, 18))

    techs = [
        ("Platform", "64 Bit, 2 core, 2.0 GHz or higher."),
        ("Operating System", "Windows 11 / macOS / Linux"),
        ("Front End Tools", "HTML5, Vanilla CSS3, Alpine.js"),
        ("Back End Tools", "Python 3.10+, Django 5.0.6"),
        ("Additional Libraries", "Gunicorn, WhiteNoise, ReportLab, python-barcode, qrcode, dj-database-url"),
        ("Editing Tool", "Visual Studio Code"),
        ("Browser", "Google Chrome, Mozilla Firefox, or any modern browser")
    ]
    for lbl, val in techs:
        story.append(Paragraph(f"{ARROW_BULLET} <b>{lbl}:</b> {val}", style_prof_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7 (Page No. 4): DATA FLOW DIAGRAM
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Data Flow Diagram</u>", style_h1_underlined))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Context Level DFD (Level 0)</b>", ParagraphStyle('dfd_sub', fontName=FONT_NORMAL, fontSize=11.5, leading=16, alignment=TA_CENTER, spaceAfter=14)))
    dfd0_img = create_image_flowable('docs_assets/diagram_dfd_level_0.png', max_w=490, max_h=370)
    story.append(dfd0_img)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8 (Page No. 5): ADMIN SIDE (LEVEL 1 DFD)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Admin Side</u>", style_h1_underlined))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Process Level DFD (Level 1)</b>", ParagraphStyle('dfd1_sub', fontName=FONT_NORMAL, fontSize=11.5, leading=16, alignment=TA_CENTER, spaceAfter=14)))
    dfd1_img = create_image_flowable('docs_assets/diagram_dfd_level_1.png', max_w=490, max_h=370)
    story.append(dfd1_img)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9 (Page No. 6): E-R DIAGRAM
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>E-R Diagram</u>", style_h1_underlined))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "• An entity Relationship Diagram (ERD) is a data modeling technique that graphically illustrates an information system’s entities and the relationship between those entities. An ERD is a conceptual and representation model of data used to represent the entity from work infrastructure.",
        ParagraphStyle('er_intro', fontName=FONT_NORMAL, fontSize=11, leading=16, alignment=TA_JUSTIFY, spaceAfter=14)
    ))
    er_img = create_image_flowable('docs_assets/diagram_er_model.png', max_w=490, max_h=350)
    story.append(er_img)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10 (Page No. 7): SDLC
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Software Development Life Cycle</u>", style_h1_underlined))
    story.append(Spacer(1, 10))

    sdlc_phases = [
        ("Planning and Requirement Analysis:", "This phase involves defining the project goals, gathering retail store inventory needs, and documenting enterprise POS requirements."),
        ("Design:", "The design stage focuses on creating the overall architecture, responsive glassmorphic UI, and relational database schema."),
        ("Development:", "This stage involves coding and implementing the software using Django 5.0, Python 3.10+, Alpine.js, and Vanilla CSS3."),
        ("Testing:", "Rigorous testing is conducted with 195 automated test cases to identify and resolve bugs and ensure the software meets quality standards."),
        ("Deployment:", "The software is released and deployed live on Render Cloud using Gunicorn WSGI and WhiteNoise static compression."),
        ("Maintenance:", "Ongoing support, inventory stock adjustments, and enhancements are provided to ensure the software continues to function properly.")
    ]
    for ph_title, ph_desc in sdlc_phases:
        story.append(Paragraph(f"o <b>{ph_title}</b>", ParagraphStyle('sdlc_h', fontName=FONT_NORMAL, fontSize=11.5, leading=16, spaceAfter=3)))
        story.append(Paragraph(ph_desc, ParagraphStyle('sdlc_p', fontName=FONT_NORMAL, fontSize=10.5, leading=15, leftIndent=14, spaceAfter=10)))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11 (Page No. 8): DATA DICTIONARY (ENTITIES LIST)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Data Dictionary</u>", style_h1_underlined))
    story.append(Spacer(1, 20))

    entities = ["User", "Product", "Category", "Brand", "Sale", "PurchaseOrder", "Supplier", "Employee"]
    for e in entities:
        story.append(Paragraph(f"o <u>{e}</u>", ParagraphStyle('dd_ent', fontName=FONT_NORMAL, fontSize=13, leading=22, spaceAfter=16)))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12 (Page No. 9): DATA DICTIONARY (USER & PRODUCT TABLES)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>User Table</b>", ParagraphStyle('tbl_title', fontName=FONT_BOLD, fontSize=15, leading=19, alignment=TA_CENTER, spaceAfter=8)))

    user_tbl_data = [
        ["Field Name", "Data Type", "Constraints"],
        ["_id", "BigAutoField", "Primary Key"],
        ["name", "String", "NOT NULL"],
        ["username", "String", "Unique, NOT NULL"],
        ["phone", "String", "NOT NULL"],
        ["role", "String", "NOT NULL"],
        ["country", "String", "NOT NULL"],
        ["password", "String", "NOT NULL"],
        ["resetOtp", "String", "Optional"],
        ["resetOtpExpiry", "Date", "Optional"],
    ]
    t_user = Table(user_tbl_data, colWidths=[140, 160, 180])
    t_user.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NORMAL),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F2F2')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_user)

    story.append(Spacer(1, 16))
    story.append(Paragraph("<b>Product Table</b>", ParagraphStyle('tbl_title', fontName=FONT_BOLD, fontSize=15, leading=19, alignment=TA_CENTER, spaceAfter=8)))

    prod_tbl_data = [
        ["Field Name", "Data Type", "Constraints"],
        ["_id", "BigAutoField", "Primary Key"],
        ["name", "String", "Unique, NOT NULL"],
        ["product_code", "String", "Unique SKU (FIM-XXXXXX)"],
        ["barcode_number", "String", "Unique EAN-13"],
        ["category_id", "ForeignKey", "References Category"],
        ["selling_price", "Decimal", "NOT NULL"],
        ["stock_quantity", "Integer", "Default 0"],
        ["createdAt", "Date", "Auto Generated"],
        ["updatedAt", "Date", "Auto Generated"],
    ]
    t_prod = Table(prod_tbl_data, colWidths=[140, 160, 180])
    t_prod.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NORMAL),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F2F2')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_prod)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13 (Page No. 10): TEST CASES
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Test Cases</u>", style_h1_underlined))
    story.append(Spacer(1, 10))

    test_tbl_data = [
        ["Case Name", "Case Description", "Actual Output", "Test Result"],
        ["User\nRegistration", "Verify user registration with valid details.", "User account created and\nredirected to login page.", "Pass"],
        ["User Login", "Verify user login functionality with valid\ncredentials.", "Redirects to user dashboard\nsuccessfully.", "Pass"],
        ["Invalid Login", "Verify login with incorrect email or pass-\nword.", "Error message displayed: \"Invalid\ncredentials\".", "Pass"],
        ["Add Product to\nCatalog", "Verify user can add a product to store\ncatalog.", "Selected product added to catalog\nwith barcode.", "Pass"],
        ["Duplicate\nProduct Check", "Verify adding product with existing name\nthrows error.", "Validation error: \"Product with\nthis name already exists\".", "Pass"],
        ["View Product\nDetails", "Verify user can view detailed product infor-\nmation.", "Product details page displayed with\nprice and barcode.", "Pass"],
        ["View\nDashboard", "Verify dashboard loads sales metrics\nand recent activity.", "Dashboard displays sales totals\nand stock alerts.", "Pass"],
        ["POS Checkout\n(Barcode)", "Verify scanning barcode sticker in POS\nterminal.", "Product added to cart; stock\ndecremented on pay.", "Pass"],
        ["Hold Sale (F8)", "Verify suspending transaction with F8\nhotkey.", "Cart cached in local storage;\ncounter cleared.", "Pass"],
        ["Admin Login", "Verify admin login functionality with valid\ncredentials.", "Redirects to admin dashboard suc-\ncessfully.", "Pass"],
    ]
    t_test = Table(test_tbl_data, colWidths=[90, 175, 155, 60])
    t_test.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), FONT_NORMAL),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F2F2')),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(t_test)
    story.append(PageBreak())

    # =========================================================================
    # PAGES 14 TO 34 (Pages No. 11 to 31): 21 SCREENSHOT PAGES!
    # =========================================================================
    screenshots_data = [
        # 1. Login Page (Has "Screen Shots" main title on Page 14)
        ("Login Page:", "pdf_report_assets/screen_01_login.png", [
            "This is the login page of the website.",
            "Users can enter their email address and password to securely access their account.",
            "After successful login, the user is redirected to the dashboard to view stock predictions and market insights."
        ], True),
        # 2. Registration Page
        ("Registration Page:", "pdf_report_assets/screen_02_register.png", [
            "This is the registration page of the website.",
            "New users can create an account by entering details like full name, email address, phone number, profession, and country.",
            "The system validates all inputs and redirects to the portal upon successful creation."
        ], False),
        # 3. User Management Page
        ("User Management Page:", "pdf_report_assets/screen_05_user_list.png", [
            "This is the user management and staff directory page of the website.",
            "Admin can view all registered staff members with their role tags and active status.",
            "Provides secure administrative controls to manage accounts and user privileges."
        ], False),
        # 4. Admin Password Reset Page
        ("Admin Password Change Page:", "pdf_report_assets/screen_06_admin_pwd.png", [
            "This is the admin password override page of the website.",
            "Super Admin can securely reset passwords for cashiers, managers, and employees.",
            "Ensures strict identity verification and business data protection."
        ], False),
        # 5. User Profile Page
        ("Profile Page:", "pdf_report_assets/screen_07_profile.png", [
            "This is the profile page of the website.",
            "Users can view and update personal details like name, email, phone, and avatar image.",
            "Users can also change their password and save profile changes easily."
        ], False),
        # 6. Dashboard Page
        ("Dashboard Page:", "pdf_report_assets/screen_03_dashboard_light.png", [
            "This is the dashboard page of the website.",
            "Users can view sales revenue trends, inventory alerts, and key business indices.",
            "It helps store managers understand operations and make better business decisions."
        ], False),
        # 7. Recent Activity Page
        ("Recent Activity Page:", "pdf_report_assets/screen_04_recent_activity.png", [
            "This section shows the real-time activity and audit feed of the platform.",
            "Users can view stock additions, recent sales, and cashier logins with timestamps.",
            "It helps supervisors monitor transactions and audit store movements easily."
        ], False),
        # 8. POS Terminal Page
        ("POS Terminal Page:", "pdf_report_assets/screen_08_pos_terminal.png", [
            "This is the Point of Sale terminal page of the website.",
            "Users can view all hardware products, category tabs, and real-time inventory counts.",
            "Cashiers can select items, adjust quantities, and calculate 18% GST in real time."
        ], False),
        # 9. POS Search Feature
        ("POS Search Feature:", "docs_assets/screenshot_pos_search.png", [
            "This is the instant product search and barcode scanner listener of the POS terminal.",
            "Users can search and filter hardware items by brand or keyword in sub-milliseconds.",
            "It displays item image, price, stock status, and + Add button for rapid checkout."
        ], False),
        # 10. POS Cart & Payment Modes
        ("POS Cart & Payment Modes:", "docs_assets/screenshot_pos_terminal.png", [
            "This section displays the interactive cart and multi-mode payment options.",
            "Cashiers can adjust quantities, apply item discounts, and select Cash, Card, or UPI.",
            "Supports instant calculation of tendered amount and customer change balance."
        ], False),
        # 11. Sales Invoices Page
        ("Sales Invoices Page:", "docs_assets/screenshot_sales_invoices.png", [
            "This is the sales invoices master ledger page of the website.",
            "Invoices are assigned clean sequential numbering (INV-26-01, INV-26-02...).",
            "Managers can inspect line items, payment status, and print A4 or thermal receipts."
        ], False),
        # 12. Products Catalog Page
        ("Products Catalog Page:", "pdf_report_assets/screen_09_products_list.png", [
            "This is the master product catalog management page of the website.",
            "Users can view all products added to inventory along with cost and selling price.",
            "Users can also edit items, generate barcodes, and monitor low-stock thresholds."
        ], False),
        # 13. Add Product Page
        ("Add Product Page:", "pdf_report_assets/screen_10_product_form.png", [
            "This is the product creation and catalog update page of the website.",
            "Enforces strict duplicate product name prevention through case-insensitive checks.",
            "Automatically generates unique SKU codes (FIM-XXXXXX) and EAN-13 barcodes."
        ], False),
        # 14. Categories Page
        ("Product Categories Page:", "pdf_report_assets/screen_11_categories.png", [
            "This is the product categories gallery page of the website.",
            "Organizes items into Laptops, Processors, GPUs, RAM, Monitors, and Cabinets.",
            "Each category includes thumbnail branding and active catalog product counters."
        ], False),
        # 15. Brands Page
        ("Hardware Brands Page:", "pdf_report_assets/screen_12_brands.png", [
            "This is the hardware manufacturer brands management page of the website.",
            "Tracks industry brands like ASUS, MSI, HP, Dell, Intel, AMD, and NVIDIA.",
            "Links brand logos and official websites directly to product listings."
        ], False),
        # 16. Purchase Orders Page
        ("Purchase Orders Page:", "pdf_report_assets/screen_13_purchase_orders.png", [
            "This is the procurement and purchase orders master page of the website.",
            "Uses sequential PO numbering (PO-26-01...) with supplier bill number tracking.",
            "Displays total invoice value, disbursed payments, and current order status."
        ], False),
        # 17. Add Purchase Order Page
        ("Add Purchase Order Page:", "pdf_report_assets/screen_14_purchase_create.png", [
            "This is the new stock procurement purchase order creation form.",
            "Creating a PO automatically credits inventory stock without extra receiving forms.",
            "Tracks itemized cost prices, tax percentages, and expected delivery dates."
        ], False),
        # 18. Supplier Bill & Payment Report
        ("Supplier Bill & Payment Report:", "pdf_report_assets/screen_15_supplier_report.png", [
            "This is the advanced supplier ledger and bill reconciliation report.",
            "Provides complete visibility into total procurement, paid amounts, and balances.",
            "Offers multi-criteria filtering by supplier, status, date, and 1-click PDF export."
        ], False),
        # 19. Settings & Branding Page
        ("Settings & Branding Page:", "pdf_report_assets/screen_16_settings.png", [
            "This is the enterprise company settings and branding page of the website.",
            "Admin can upload custom company logos with live instant thumbnail preview.",
            "Configures store contact information, GST number, currency, and theme colors."
        ], False),
        # 20. Employee Attendance Page
        ("Employee Attendance Page:", "pdf_report_assets/screen_17_attendance.png", [
            "This is the staff attendance tracking and HR management page of the website.",
            "Managers can mark Present, Absent, Half-Day, or Leave with duplicate prevention.",
            "Summarizes monthly working hours and attendance records for payroll auditing."
        ], False),
        # 21. Staff Leave Management Page
        ("Staff Leave Management Page:", "pdf_report_assets/screen_18_leaves.png", [
            "This is the employee leave management and approval dashboard page.",
            "Employees can apply for Casual, Sick, or Annual leave with date range selection.",
            "Store managers can review, approve, or reject pending leave applications."
        ], False),
    ]

    for title, img_path, bullets, is_first in screenshots_data:
        story.append(Spacer(1, 10))
        if is_first:
            story.append(Paragraph("<u>Screen Shots</u>", style_screen_main_title))
            story.append(Spacer(1, 4))
        story.append(Paragraph(f"<u>{title}</u>", style_screen_sub_title))
        story.append(Spacer(1, 4))
        img_flowable = create_image_flowable(img_path, max_w=490, max_h=260)
        story.append(img_flowable)
        story.append(Spacer(1, 16))
        for b in bullets:
            story.append(Paragraph(f"{ARROW_BULLET} {b}", style_scr_bullet))
        story.append(PageBreak())

    # =========================================================================
    # PAGE 35 (Page No. 32): FUTURE ENHANCEMENT
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Future Enhancement</u>", style_h1_underlined))
    story.append(Spacer(1, 20))

    enhancements = [
        "Add real-time trading and multi-branch store synchronization across multiple retail outlets.",
        "Implement advanced AI models for inventory demand forecasting based on seasonal hardware releases.",
        "Provide mobile application support (Android and iOS) for barcode scanning and on-the-go cashiering.",
        "Add automated customer loyalty reward tiers with dynamic discount coupon code generation.",
        "Enable notifications and alerts for price changes, low-stock reorders, and supplier payment dues.",
        "Introduce automated GST tax filing export (GSTR-1 and GSTR-3B) with one-click reconciliation."
    ]
    for enh in enhancements:
        story.append(Paragraph(f"{DIAMOND_BULLET} {enh}", style_req_bullet))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 36 (Page No. 33): WEBLIOGRAPHY
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>Webliography</u>", style_h1_underlined))
    story.append(Spacer(1, 25))

    links = [
        "https://tailwindcss.com/",
        "https://www.djangoproject.com/",
        "https://www.python.org/",
        "https://alpinejs.dev/",
        "https://render.com/"
    ]
    for lnk in links:
        story.append(Paragraph(f"{ARROW_BULLET} <u>{lnk}</u>", ParagraphStyle('web_p', fontName=FONT_NORMAL, fontSize=12, leading=22, spaceAfter=22)))

    # Build the document
    doc.build(story, onFirstPage=draw_decorations, onLaterPages=draw_decorations)
    print(f"[SUCCESS] Built {pdf_path} with EXACT layout and 36 pages!")

if __name__ == '__main__':
    build_pdf()
