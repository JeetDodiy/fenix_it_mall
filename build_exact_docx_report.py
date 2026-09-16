import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

# ECMA-376 strict schema sequence definitions to prevent Word corruption warnings
SECTPR_ORDER = [
    'headerReference', 'footerReference', 'type', 'pgSz', 'pgMar', 'paperSrc',
    'pgBorders', 'lnNumType', 'pgNumType', 'cols', 'formProt', 'vAlign',
    'noEndnote', 'titlePg', 'textDirection', 'bidi', 'rtlGutter', 'docGrid', 'printerSettings'
]

TBLPR_ORDER = [
    'tblStyle', 'tblpPr', 'tblOverlap', 'bidiVisual', 'tblStyleRowBandSize',
    'tblStyleColBandSize', 'tblW', 'jc', 'tblCellSpacing', 'tblInd', 'tblBorders',
    'shd', 'tblLayout', 'tblCellMar', 'tblLook', 'tblCaption', 'tblDescription', 'tblPrChange'
]

TCPR_ORDER = [
    'tcW', 'gridSpan', 'hMerge', 'vMerge', 'tcBorders', 'shd', 'noWrap',
    'tcMar', 'textDirection', 'tcFitText', 'vAlign', 'hideMark', 'headers',
    'cellIns', 'cellDel', 'cellMerge', 'tcPrChange'
]

def reorder_children(parent, order_list):
    """Sort XML child elements strictly by ECMA-376 schema sequence."""
    children = list(parent)
    def sort_key(elem):
        tag = elem.tag.split('}')[-1]
        try:
            return order_list.index(tag)
        except ValueError:
            return 999
    sorted_children = sorted(children, key=sort_key)
    for c in children:
        parent.remove(c)
    for c in sorted_children:
        parent.append(c)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_double_page_borders(section):
    sectPr = section._sectPr
    pgBorders = parse_xml(f'''
        <w:pgBorders {nsdecls("w")} w:offsetFrom="page">
            <w:top w:val="double" w:sz="18" w:space="24" w:color="000000"/>
            <w:left w:val="double" w:sz="18" w:space="24" w:color="000000"/>
            <w:bottom w:val="double" w:sz="18" w:space="24" w:color="000000"/>
            <w:right w:val="double" w:sz="18" w:space="24" w:color="000000"/>
        </w:pgBorders>
    ''')
    sectPr.append(pgBorders)

def add_page_number(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def build_docx():
    docx_path = "Fenix_IT_Mall_Project_Report.docx"
    print(f"Building {docx_path} (Matching Brijesh_Msit_Sem_4.pdf)...")
    doc = Document()

    # Section page setup: A4
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)

    # Double page border
    add_double_page_borders(section)

    # Header: "Fenix IT Mall" top-left
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "Fenix IT Mall"
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in hp.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)

    # Footer: page number centered
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run()
    frun.font.name = "Times New Roman"
    frun.font.size = Pt(10.5)
    add_page_number(frun)

    # Normal style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # Helper: add centered underlined heading
    def add_heading_u(text, pt=18, space_after=14):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.underline = True
        run.font.size = Pt(pt)
        return p

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("A PROJECT REPORT ON")
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(28)
    r = p.add_run("Fenix IT Mall")
    r.bold = True
    r.font.size = Pt(26)
    r.font.color.rgb = RGBColor(0x4A, 0x90, 0xE2)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("SUBMITTED TO:")
    r.bold = True
    r.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(26)
    r = p.add_run("Geetanjali College of Computer Science and Commerce (BBA) Saurashtra University Rajkot")
    r.bold = True
    r.font.size = Pt(12.5)

    cover_specs = [
        ("FRONT END :", "HTML5, Vanilla CSS3, Alpine.js"),
        ("BACK END :", "Python 3.10+, Django 5.0"),
        ("AFFILIATED BY :", "Saurashtra University"),
        ("ACADEMIC YEAR :", "2025-2026")
    ]
    for lbl, val in cover_specs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(lbl)
        r.bold = True
        r.font.size = Pt(13)

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(16)
        r = p.add_run(val)
        r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("PROJECT GUIDE:")
    r.bold = True
    r.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("Prof. Harsh Joshi")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0x4A, 0x90, 0xE2)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("PREPARED BY:")
    r.bold = True
    r.font.size = Pt(13)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Jeet Dodiya")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0x4A, 0x90, 0xE2)

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: ACKNOWLEDGEMENT
    # =========================================================================
    add_heading_u("Acknowledgement", pt=18, space_after=18)

    ack_texts = [
        "First and foremost, we are sincerely thankful to Saurashtra University for giving us the opportunity to work on this project as part of our curriculum.",
        "We extend our gratitude to Geetanjali Group Of Colleges for providing us with the resources and environment needed to develop our project.",
        "We are particularly grateful to our Head of Department, Prof. Brijesh Shah for their constant support and guidance throughout the project.",
        "We would like to express our deepest appreciation to our project guide, prof. Kishorsinh Vala, who guided us through the analysis and development phases of our project, providing invaluable advice and support.",
        "We are also thankful to all well-wishers and friends who supported us during the project development."
    ]
    for txt in ack_texts:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.line_spacing = Pt(18)
        r = p.add_run(f"• {txt}")
        r.font.size = Pt(11.5)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(30)
    p.paragraph_format.left_indent = Inches(0.4)
    r = p.add_run("Yours Faithfully,\n\n")
    r.font.size = Pt(11.5)
    r2 = p.add_run("Jeet Dodiya")
    r2.bold = True
    r2.font.size = Pt(11.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: INDEX
    # =========================================================================
    add_heading_u("Index", pt=18, space_after=18)

    index_data = [
        ("SR.NO", "TOPICNAME", "PAGENO."),
        ("1", "Project Profile", "1"),
        ("2", "Project Requirement", "2"),
        ("3", "Technology Requirement", "3"),
        ("4", "Data Flow Diagram", "4"),
        ("5", "E-R Diagram", "6"),
        ("6", "SDLC", "7"),
        ("7", "Data Dictionary", "8"),
        ("8", "Test cases", "10"),
        ("9", "Screenshots", "11"),
        ("10", "Future Enhancement of project", "32"),
        ("11", "Webliography", "33"),
    ]
    t_idx = doc.add_table(rows=len(index_data), cols=3)
    t_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(1.0), Inches(4.5), Inches(1.0)]

    for row_idx, row in enumerate(index_data):
        for col_idx, text in enumerate(row):
            cell = t_idx.cell(row_idx, col_idx)
            cell.width = col_w[col_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_after = Pt(8)
            cp.paragraph_format.space_before = Pt(8)
            if col_idx == 0 or col_idx == 2:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = cp.add_run(text)
            r.font.size = Pt(11)
            if row_idx == 0:
                r.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 4 (p. 1): PROJECT PROFILE
    # =========================================================================
    add_heading_u("Project Profile", pt=18, space_after=22)

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
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.line_spacing = Pt(20)
        r1 = p.add_run("➢ ")
        r1.font.name = "Segoe UI Symbol"
        r1.font.size = Pt(12)
        r2 = p.add_run(f"{lbl}: ")
        r2.bold = True
        r2.font.size = Pt(12)
        r3 = p.add_run(val)
        r3.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5 (p. 2): PROJECT REQUIREMENT
    # =========================================================================
    add_heading_u("Project Requirement", pt=18, space_after=28)

    reqs = [
        ("Processor", "Intel Core i3 or higher"),
        ("RAM", "4 GB or more"),
        ("Hard Disk", "500 GB or more")
    ]
    for lbl, val in reqs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(24)
        p.paragraph_format.line_spacing = Pt(22)
        r1 = p.add_run("❖ ")
        r1.font.name = "Segoe UI Symbol"
        r1.font.size = Pt(12.5)
        r2 = p.add_run(f"{lbl}: ")
        r2.bold = True
        r2.font.size = Pt(12.5)
        r3 = p.add_run(val)
        r3.font.size = Pt(12.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6 (p. 3): TECHNOLOGY REQUIREMENT
    # =========================================================================
    add_heading_u("Technology Requirement", pt=18, space_after=22)

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
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.line_spacing = Pt(20)
        r1 = p.add_run("➢ ")
        r1.font.name = "Segoe UI Symbol"
        r1.font.size = Pt(12)
        r2 = p.add_run(f"{lbl}: ")
        r2.bold = True
        r2.font.size = Pt(12)
        r3 = p.add_run(val)
        r3.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 7 (p. 4): DATA FLOW DIAGRAM
    # =========================================================================
    add_heading_u("Data Flow Diagram", pt=18, space_after=10)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("Context Level DFD (Level 0)")
    r.bold = True
    r.font.size = Pt(12)

    if os.path.exists('docs_assets/diagram_dfd_level_0.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture('docs_assets/diagram_dfd_level_0.png', width=Inches(6.0))

    doc.add_page_break()

    # =========================================================================
    # PAGE 8 (p. 5): ADMIN SIDE
    # =========================================================================
    add_heading_u("Admin Side", pt=18, space_after=10)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("Process Level DFD (Level 1)")
    r.bold = True
    r.font.size = Pt(12)

    if os.path.exists('docs_assets/diagram_dfd_level_1.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture('docs_assets/diagram_dfd_level_1.png', width=Inches(6.0))

    doc.add_page_break()

    # =========================================================================
    # PAGE 9 (p. 6): E-R DIAGRAM
    # =========================================================================
    add_heading_u("E-R Diagram", pt=18, space_after=10)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = Pt(16)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run("• An entity Relationship Diagram (ERD) is a data modeling technique that graphically illustrates an information system’s entities and the relationship between those entities. An ERD is a conceptual and representation model of data used to represent the entity from work infrastructure.")
    r.font.size = Pt(11)

    if os.path.exists('docs_assets/diagram_er_model.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture('docs_assets/diagram_er_model.png', width=Inches(6.0))

    doc.add_page_break()

    # =========================================================================
    # PAGE 10 (p. 7): SDLC
    # =========================================================================
    add_heading_u("Software Development Life Cycle", pt=18, space_after=14)

    sdlc_phases = [
        ("Planning and Requirement Analysis:", "This phase involves defining the project goals, gathering retail store inventory needs, and documenting enterprise POS requirements."),
        ("Design:", "The design stage focuses on creating the overall architecture, responsive glassmorphic UI, and relational database schema."),
        ("Development:", "This stage involves coding and implementing the software using Django 5.0, Python 3.10+, Alpine.js, and Vanilla CSS3."),
        ("Testing:", "Rigorous testing is conducted with 195 automated test cases to identify and resolve bugs and ensure the software meets quality standards."),
        ("Deployment:", "The software is released and deployed live on Render Cloud using Gunicorn WSGI and WhiteNoise static compression."),
        ("Maintenance:", "Ongoing support, inventory stock adjustments, and enhancements are provided to ensure the software continues to function properly.")
    ]
    for ph_title, ph_desc in sdlc_phases:
        p1 = doc.add_paragraph()
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(f"o {ph_title}")
        r1.bold = True
        r1.font.size = Pt(11.5)

        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.25)
        p2.paragraph_format.space_after = Pt(10)
        p2.paragraph_format.line_spacing = Pt(15)
        r2 = p2.add_run(ph_desc)
        r2.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 11 (p. 8): DATA DICTIONARY (ENTITIES LIST)
    # =========================================================================
    add_heading_u("Data Dictionary", pt=18, space_after=24)

    entities = ["User", "Product", "Category", "Brand", "Sale", "PurchaseOrder", "Supplier", "Employee"]
    for e in entities:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(16)
        p.paragraph_format.line_spacing = Pt(22)
        r = p.add_run("o ")
        r.font.size = Pt(13)
        r2 = p.add_run(e)
        r2.underline = True
        r2.font.size = Pt(13)

    doc.add_page_break()

    # =========================================================================
    # PAGE 12 (p. 9): USER & PRODUCT TABLES
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("User Table")
    r.bold = True
    r.font.size = Pt(14)

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
    t_u = doc.add_table(rows=len(user_tbl_data), cols=3)
    t_u.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_u)
    u_widths = [Inches(2.0), Inches(2.2), Inches(2.4)]
    for ri, row in enumerate(user_tbl_data):
        for ci, val in enumerate(row):
            cell = t_u.cell(ri, ci)
            cell.width = u_widths[ci]
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if ri == 0:
                set_cell_background(cell, "F2F2F2")
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_after = Pt(2)
            cp.paragraph_format.space_before = Pt(2)
            run = cp.add_run(val)
            run.font.size = Pt(9.5)
            if ri == 0:
                run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("Product Table")
    r.bold = True
    r.font.size = Pt(14)

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
    t_p = doc.add_table(rows=len(prod_tbl_data), cols=3)
    t_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_p)
    for ri, row in enumerate(prod_tbl_data):
        for ci, val in enumerate(row):
            cell = t_p.cell(ri, ci)
            cell.width = u_widths[ci]
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if ri == 0:
                set_cell_background(cell, "F2F2F2")
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_after = Pt(2)
            cp.paragraph_format.space_before = Pt(2)
            run = cp.add_run(val)
            run.font.size = Pt(9.5)
            if ri == 0:
                run.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 13 (p. 10): TEST CASES
    # =========================================================================
    add_heading_u("Test Cases", pt=18, space_after=12)

    test_tbl_data = [
        ["Case Name", "Case Description", "Actual Output", "Test Result"],
        ["User Registration", "Verify user registration with valid details.", "User account created and redirected to login page.", "Pass"],
        ["User Login", "Verify user login functionality with valid credentials.", "Redirects to user dashboard successfully.", "Pass"],
        ["Invalid Login", "Verify login with incorrect email or password.", "Error message displayed: \"Invalid credentials\".", "Pass"],
        ["Add Product to Catalog", "Verify user can add a product to store catalog.", "Selected product added to catalog with barcode.", "Pass"],
        ["Duplicate Product Check", "Verify adding product with existing name throws error.", "Validation error: \"Product with this name already exists\".", "Pass"],
        ["View Product Details", "Verify user can view detailed product information.", "Product details page displayed with price and barcode.", "Pass"],
        ["View Dashboard", "Verify dashboard loads sales metrics and recent activity.", "Dashboard displays sales totals and stock alerts.", "Pass"],
        ["POS Checkout (Barcode)", "Verify scanning barcode sticker in POS terminal.", "Product added to cart; stock decremented on pay.", "Pass"],
        ["Hold Sale (F8)", "Verify suspending transaction with F8 hotkey.", "Cart cached in local storage; counter cleared.", "Pass"],
        ["Admin Login", "Verify admin login functionality with valid credentials.", "Redirects to admin dashboard successfully.", "Pass"],
    ]
    t_tc = doc.add_table(rows=len(test_tbl_data), cols=4)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tc)
    tc_widths = [Inches(1.4), Inches(2.4), Inches(2.2), Inches(0.6)]
    for ri, row in enumerate(test_tbl_data):
        for ci, val in enumerate(row):
            cell = t_tc.cell(ri, ci)
            cell.width = tc_widths[ci]
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            if ri == 0:
                set_cell_background(cell, "F2F2F2")
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_after = Pt(2)
            cp.paragraph_format.space_before = Pt(2)
            if ci == 3:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cp.add_run(val)
            run.font.size = Pt(9)
            if ri == 0:
                run.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGES 14 TO 34: 21 SCREENSHOT PAGES
    # =========================================================================
    screenshots_data = [
        ("Login Page:", "pdf_report_assets/screen_01_login.png", [
            "This is the login page of the website.",
            "Users can enter their email address and password to securely access their account.",
            "After successful login, the user is redirected to the dashboard to view stock predictions and market insights."
        ], True),
        ("Registration Page:", "pdf_report_assets/screen_02_register.png", [
            "This is the registration page of the website.",
            "New users can create an account by entering details like full name, email address, phone number, profession, and country.",
            "The system validates all inputs and redirects to the portal upon successful creation."
        ], False),
        ("User Management Page:", "pdf_report_assets/screen_05_user_list.png", [
            "This is the user management and staff directory page of the website.",
            "Admin can view all registered staff members with their role tags and active status.",
            "Provides secure administrative controls to manage accounts and user privileges."
        ], False),
        ("Admin Password Change Page:", "pdf_report_assets/screen_06_admin_pwd.png", [
            "This is the admin password override page of the website.",
            "Super Admin can securely reset passwords for cashiers, managers, and employees.",
            "Ensures strict identity verification and business data protection."
        ], False),
        ("Profile Page:", "pdf_report_assets/screen_07_profile.png", [
            "This is the profile page of the website.",
            "Users can view and update personal details like name, email, phone, and avatar image.",
            "Users can also change their password and save profile changes easily."
        ], False),
        ("Dashboard Page:", "pdf_report_assets/screen_03_dashboard_light.png", [
            "This is the dashboard page of the website.",
            "Users can view sales revenue trends, inventory alerts, and key business indices.",
            "It helps store managers understand operations and make better business decisions."
        ], False),
        ("Recent Activity Page:", "pdf_report_assets/screen_04_recent_activity.png", [
            "This section shows the real-time activity and audit feed of the platform.",
            "Users can view stock additions, recent sales, and cashier logins with timestamps.",
            "It helps supervisors monitor transactions and audit store movements easily."
        ], False),
        ("POS Terminal Page:", "pdf_report_assets/screen_08_pos_terminal.png", [
            "This is the Point of Sale terminal page of the website.",
            "Users can view all hardware products, category tabs, and real-time inventory counts.",
            "Cashiers can select items, adjust quantities, and calculate 18% GST in real time."
        ], False),
        ("POS Search Feature:", "docs_assets/screenshot_pos_search.png", [
            "This is the instant product search and barcode scanner listener of the POS terminal.",
            "Users can search and filter hardware items by brand or keyword in sub-milliseconds.",
            "It displays item image, price, stock status, and + Add button for rapid checkout."
        ], False),
        ("POS Cart & Payment Modes:", "docs_assets/screenshot_pos_terminal.png", [
            "This section displays the interactive cart and multi-mode payment options.",
            "Cashiers can adjust quantities, apply item discounts, and select Cash, Card, or UPI.",
            "Supports instant calculation of tendered amount and customer change balance."
        ], False),
        ("Sales Invoices Page:", "docs_assets/screenshot_sales_invoices.png", [
            "This is the sales invoices master ledger page of the website.",
            "Invoices are assigned clean sequential numbering (INV-26-01, INV-26-02...).",
            "Managers can inspect line items, payment status, and print A4 or thermal receipts."
        ], False),
        ("Products Catalog Page:", "pdf_report_assets/screen_09_products_list.png", [
            "This is the master product catalog management page of the website.",
            "Users can view all products added to inventory along with cost and selling price.",
            "Users can also edit items, generate barcodes, and monitor low-stock thresholds."
        ], False),
        ("Add Product Page:", "pdf_report_assets/screen_10_product_form.png", [
            "This is the product creation and catalog update page of the website.",
            "Enforces strict duplicate product name prevention through case-insensitive checks.",
            "Automatically generates unique SKU codes (FIM-XXXXXX) and EAN-13 barcodes."
        ], False),
        ("Product Categories Page:", "pdf_report_assets/screen_11_categories.png", [
            "This is the product categories gallery page of the website.",
            "Organizes items into Laptops, Processors, GPUs, RAM, Monitors, and Cabinets.",
            "Each category includes thumbnail branding and active catalog product counters."
        ], False),
        ("Hardware Brands Page:", "pdf_report_assets/screen_12_brands.png", [
            "This is the hardware manufacturer brands management page of the website.",
            "Tracks industry brands like ASUS, MSI, HP, Dell, Intel, AMD, and NVIDIA.",
            "Links brand logos and official websites directly to product listings."
        ], False),
        ("Purchase Orders Page:", "pdf_report_assets/screen_13_purchase_orders.png", [
            "This is the procurement and purchase orders master page of the website.",
            "Uses sequential PO numbering (PO-26-01...) with supplier bill number tracking.",
            "Displays total invoice value, disbursed payments, and current order status."
        ], False),
        ("Add Purchase Order Page:", "pdf_report_assets/screen_14_purchase_create.png", [
            "This is the new stock procurement purchase order creation form.",
            "Creating a PO automatically credits inventory stock without extra receiving forms.",
            "Tracks itemized cost prices, tax percentages, and expected delivery dates."
        ], False),
        ("Supplier Bill & Payment Report:", "pdf_report_assets/screen_15_supplier_report.png", [
            "This is the advanced supplier ledger and bill reconciliation report.",
            "Provides complete visibility into total procurement, paid amounts, and balances.",
            "Offers multi-criteria filtering by supplier, status, date, and 1-click PDF export."
        ], False),
        ("Settings & Branding Page:", "pdf_report_assets/screen_16_settings.png", [
            "This is the enterprise company settings and branding page of the website.",
            "Admin can upload custom company logos with live instant thumbnail preview.",
            "Configures store contact information, GST number, currency, and theme colors."
        ], False),
        ("Employee Attendance Page:", "pdf_report_assets/screen_17_attendance.png", [
            "This is the staff attendance tracking and HR management page of the website.",
            "Managers can mark Present, Absent, Half-Day, or Leave with duplicate prevention.",
            "Summarizes monthly working hours and attendance records for payroll auditing."
        ], False),
        ("Staff Leave Management Page:", "pdf_report_assets/screen_18_leaves.png", [
            "This is the employee leave management and approval dashboard page.",
            "Employees can apply for Casual, Sick, or Annual leave with date range selection.",
            "Store managers can review, approve, or reject pending leave applications."
        ], False),
    ]

    for title, img_path, bullets, is_first in screenshots_data:
        if is_first:
            add_heading_u("Screen Shots", pt=18, space_after=8)
        
        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_sub.paragraph_format.space_before = Pt(4)
        p_sub.paragraph_format.space_after = Pt(8)
        r = p_sub.add_run(title)
        r.bold = True
        r.underline = True
        r.font.size = Pt(14)

        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(12)
            p_img.add_run().add_picture(img_path, width=Inches(6.0))

        for b in bullets:
            p_b = doc.add_paragraph()
            p_b.paragraph_format.space_after = Pt(7)
            p_b.paragraph_format.line_spacing = Pt(17)
            r1 = p_b.add_run("➢ ")
            r1.font.name = "Segoe UI Symbol"
            r1.font.size = Pt(11.5)
            r2 = p_b.add_run(b)
            r2.font.size = Pt(11.5)

        doc.add_page_break()

    # =========================================================================
    # PAGE 35 (p. 32): FUTURE ENHANCEMENT
    # =========================================================================
    add_heading_u("Future Enhancement", pt=18, space_after=24)

    enhancements = [
        "Add real-time trading and multi-branch store synchronization across multiple retail outlets.",
        "Implement advanced AI models for inventory demand forecasting based on seasonal hardware releases.",
        "Provide mobile application support (Android and iOS) for barcode scanning and on-the-go cashiering.",
        "Add automated customer loyalty reward tiers with dynamic discount coupon code generation.",
        "Enable notifications and alerts for price changes, low-stock reorders, and supplier payment dues.",
        "Introduce automated GST tax filing export (GSTR-1 and GSTR-3B) with one-click reconciliation."
    ]
    for enh in enhancements:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(22)
        p.paragraph_format.line_spacing = Pt(22)
        r1 = p.add_run("❖ ")
        r1.font.name = "Segoe UI Symbol"
        r1.font.size = Pt(12.5)
        r2 = p.add_run(enh)
        r2.font.size = Pt(12.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 36 (p. 33): WEBLIOGRAPHY
    # =========================================================================
    add_heading_u("Webliography", pt=18, space_after=28)

    links = [
        "https://tailwindcss.com/",
        "https://www.djangoproject.com/",
        "https://www.python.org/",
        "https://alpinejs.dev/",
        "https://render.com/"
    ]
    for lnk in links:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(22)
        p.paragraph_format.line_spacing = Pt(22)
        r1 = p.add_run("➢ ")
        r1.font.name = "Segoe UI Symbol"
        r1.font.size = Pt(12)
        r2 = p.add_run(lnk)
        r2.underline = True
        r2.font.size = Pt(12)

    # STRICT ECMA-376 REORDERING PASS:
    # Ensure all XML elements inside sectPr, tblPr, and tcPr strictly follow ECMA-376 sequence
    reorder_children(doc.sections[0]._sectPr, SECTPR_ORDER)
    for t in doc.tables:
        reorder_children(t._tbl.tblPr, TBLPR_ORDER)
        for row in t.rows:
            for cell in row.cells:
                tcPr = cell._tc.find(qn('w:tcPr'))
                if tcPr is not None:
                    reorder_children(tcPr, TCPR_ORDER)

    doc.save(docx_path)
    print(f"[SUCCESS] Built {docx_path} with 100% ECMA-376 compliant layout and 36 pages!")

if __name__ == '__main__':
    build_docx()
