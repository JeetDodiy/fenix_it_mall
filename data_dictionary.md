# DATA DICTIONARY
## Project: Fenix IT Mall — Inventory Management System

---

| | |
|---|---|
| **Document Title** | Data Dictionary |
| **Project Name** | Fenix IT Mall |
| **Application Type** | Inventory Management System |
| **Framework** | Django (Python) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Total Tables** | 20 |

---

## TABLE OF CONTENTS

1. [accounts_customuser](#1-accounts_customuser)
2. [products_category](#2-products_category)
3. [products_brand](#3-products_brand)
4. [products_product](#4-products_product)
5. [products_productimage](#5-products_productimage)
6. [customers_customer](#6-customers_customer)
7. [suppliers_supplier](#7-suppliers_supplier)
8. [employees_employee](#8-employees_employee)
9. [employees_attendance](#9-employees_attendance)
10. [employees_leave](#10-employees_leave)
11. [sales_sale](#11-sales_sale)
12. [sales_saleitem](#12-sales_saleitem)
13. [sales_invoiceauditlog](#13-sales_invoiceauditlog)
14. [purchase_purchaseorder](#14-purchase_purchaseorder)
15. [purchase_purchaseitem](#15-purchase_purchaseitem)
16. [purchase_supplierpayment](#16-purchase_supplierpayment)
17. [inventory_stockmovement](#17-inventory_stockmovement)
18. [inventory_stockadjustment](#18-inventory_stockadjustment)
19. [notifications_notification](#19-notifications_notification)
20. [settings_app_companysettings](#20-settings_app_companysettings)

---

## 1. `accounts_customuser`

**Description:**
Stores all system user accounts. Extends Django's built-in AbstractUser model with
role-based access control (Admin, Manager, Employee, Cashier). This table manages
who can log in and what they are allowed to do in the system.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each user |
| 2 | username | VARCHAR | 150 | NO | — | UNIQUE | Login username of the user |
| 3 | first_name | VARCHAR | 150 | YES | '' | — | First name of the user |
| 4 | last_name | VARCHAR | 150 | YES | '' | — | Last name of the user |
| 5 | email | VARCHAR | 254 | YES | '' | — | Email address of the user |
| 6 | password | VARCHAR | 128 | NO | — | — | Hashed password (auto-managed by Django) |
| 7 | is_staff | BOOLEAN | — | NO | FALSE | — | Whether user can access the admin panel |
| 8 | is_superuser | BOOLEAN | — | NO | FALSE | — | Whether user has all permissions |
| 9 | role | VARCHAR | 20 | NO | employee | — | User role: admin / manager / employee / cashier |
| 10 | phone | VARCHAR | 15 | YES | NULL | — | Contact phone number of the user |
| 11 | address | TEXT | — | YES | NULL | — | Residential address of the user |
| 12 | profile_picture | VARCHAR | 100 | YES | NULL | — | File path of profile image (upload: profiles/) |
| 13 | is_active | BOOLEAN | — | NO | TRUE | — | Whether the user account is active or disabled |
| 14 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the user record was created |
| 15 | updated_at | DATETIME | — | NO | Auto | — | Timestamp when the user record was last updated |

---

## 2. `products_category`

**Description:**
Stores product categories used to classify and organize products in the system
(e.g., Laptops, Mobile Phones, Printers, Accessories). Each product belongs to
one category.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each category |
| 2 | name | VARCHAR | 100 | NO | — | UNIQUE | Name of the product category |
| 3 | slug | VARCHAR | 100 | NO | Auto | UNIQUE | URL-friendly version of the category name |
| 4 | image | VARCHAR | 100 | YES | NULL | — | File path of category image (upload: categories/) |
| 5 | description | TEXT | — | YES | NULL | — | Detailed description of the category |
| 6 | is_active | BOOLEAN | — | NO | TRUE | — | Whether the category is currently active |
| 7 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the category was created |

---

## 3. `products_brand`

**Description:**
Stores brand or manufacturer information for products. Products can optionally be
linked to a brand (e.g., HP, Dell, Samsung, Apple, Lenovo).

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each brand |
| 2 | name | VARCHAR | 100 | NO | — | UNIQUE | Name of the brand or manufacturer |
| 3 | logo | VARCHAR | 100 | YES | NULL | — | File path of brand logo image (upload: brands/) |
| 4 | description | TEXT | — | YES | NULL | — | Brief description about the brand |
| 5 | website | VARCHAR | 200 | YES | NULL | — | Official website URL of the brand |
| 6 | is_active | BOOLEAN | — | NO | TRUE | — | Whether the brand is currently active |
| 7 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the brand record was added |

---

## 4. `products_product`

**Description:**
The central and most important table of the system. Stores complete product
information including pricing, stock levels, barcode, QR code, and foreign key
links to Category, Brand, and Supplier tables.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each product |
| 2 | name | VARCHAR | 200 | NO | — | UNIQUE | Full name of the product |
| 3 | product_code | VARCHAR | 50 | NO | Auto | UNIQUE | System-generated SKU code (format: FIM-XXXXXXXX) |
| 4 | barcode_number | VARCHAR | 50 | YES | NULL | — | Barcode value used for scanning |
| 5 | barcode_image | VARCHAR | 100 | YES | NULL | — | File path of auto-generated barcode image |
| 6 | qr_code | VARCHAR | 100 | YES | NULL | — | File path of auto-generated QR code image |
| 7 | slug | VARCHAR | 200 | NO | Auto | UNIQUE | URL-friendly unique product identifier |
| 8 | category_id | INTEGER | — | YES | NULL | FK | References products_category(id) |
| 9 | brand_id | INTEGER | — | YES | NULL | FK | References products_brand(id) |
| 10 | supplier_id | INTEGER | — | YES | NULL | FK | References suppliers_supplier(id) |
| 11 | purchase_price | DECIMAL | 10,2 | NO | 0.00 | — | Price at which the product was purchased |
| 12 | selling_price | DECIMAL | 10,2 | NO | 0.00 | — | Price at which the product is sold to customers |
| 13 | gst_percentage | DECIMAL | 5,2 | NO | 18.00 | — | GST tax percentage applicable to this product |
| 14 | description | TEXT | — | YES | NULL | — | Detailed description of the product |
| 15 | warranty | VARCHAR | 100 | YES | NULL | — | Warranty period or details of the product |
| 16 | status | VARCHAR | 20 | NO | active | — | Status: active / inactive / discontinued |
| 17 | stock_quantity | INTEGER | — | NO | 0 | — | Current available stock quantity |
| 18 | low_stock_threshold | INTEGER | — | NO | 5 | — | Minimum quantity before a low stock alert is raised |
| 19 | is_active | BOOLEAN | — | NO | TRUE | — | Whether the product is visible and listed |
| 20 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the product was added to the system |
| 21 | updated_at | DATETIME | — | NO | Auto | — | Timestamp when the product was last modified |

---

## 5. `products_productimage`

**Description:**
Stores multiple images linked to a single product. One image can be marked as
the primary or featured image. A product can have many images.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each product image |
| 2 | product_id | INTEGER | — | NO | — | FK | References products_product(id) |
| 3 | image | VARCHAR | 100 | NO | — | — | File path of the product image (upload: products/) |
| 4 | is_primary | BOOLEAN | — | NO | FALSE | — | Whether this is the main or featured product image |
| 5 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the image was uploaded |

---

## 6. `customers_customer`

**Description:**
Stores customer information for tracking sale transactions, contact details,
and loyalty reward points. Customers are linked to their purchases via the
sales_sale table.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each customer |
| 2 | name | VARCHAR | 200 | NO | — | — | Full name of the customer |
| 3 | phone | VARCHAR | 15 | NO | — | UNIQUE | Mobile or phone number of the customer |
| 4 | email | VARCHAR | 254 | YES | NULL | — | Email address of the customer |
| 5 | address | TEXT | — | YES | NULL | — | Delivery or billing address of the customer |
| 6 | reward_points | INTEGER | — | NO | 0 | — | Accumulated loyalty reward points |
| 7 | is_active | BOOLEAN | — | NO | TRUE | — | Whether the customer account is active |
| 8 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the customer was first registered |
| 9 | updated_at | DATETIME | — | NO | Auto | — | Timestamp when the customer record was last updated |

---

## 7. `suppliers_supplier`

**Description:**
Stores information about product suppliers or vendors from whom the business
purchases inventory. Suppliers are linked to products and purchase orders.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each supplier |
| 2 | company_name | VARCHAR | 200 | NO | — | — | Registered name of the supplier company |
| 3 | contact_person | VARCHAR | 100 | NO | — | — | Name of the primary contact person at the supplier |
| 4 | phone | VARCHAR | 15 | NO | — | — | Contact phone number of the supplier |
| 5 | email | VARCHAR | 254 | YES | NULL | — | Email address of the supplier |
| 6 | address | TEXT | — | YES | NULL | — | Physical or mailing address of the supplier |
| 7 | gst_number | VARCHAR | 20 | YES | NULL | — | GST registration number of the supplier |
| 8 | is_active | BOOLEAN | — | NO | TRUE | — | Whether the supplier is currently active |
| 9 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the supplier was added |
| 10 | updated_at | DATETIME | — | NO | Auto | — | Timestamp when the supplier record was last updated |

---

## 8. `employees_employee`

**Description:**
Stores all employee information including personal details, job designation,
department, salary, and joining date. An employee can optionally be linked
to a system user account (accounts_customuser).

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each employee |
| 2 | user_id | INTEGER | — | YES | NULL | FK (1-1) | References accounts_customuser(id) |
| 3 | employee_id | VARCHAR | 20 | NO | Auto | UNIQUE | System-generated employee code (format: EMP-XXXXXX) |
| 4 | first_name | VARCHAR | 100 | NO | — | — | First name of the employee |
| 5 | last_name | VARCHAR | 100 | NO | — | — | Last name of the employee |
| 6 | email | VARCHAR | 254 | YES | NULL | — | Email address of the employee |
| 7 | phone | VARCHAR | 15 | NO | — | — | Contact phone number of the employee |
| 8 | address | TEXT | — | YES | NULL | — | Residential address of the employee |
| 9 | designation | VARCHAR | 100 | NO | — | — | Job title or designation of the employee |
| 10 | department | VARCHAR | 100 | YES | NULL | — | Department the employee belongs to |
| 11 | salary | DECIMAL | 10,2 | NO | 0.00 | — | Monthly salary of the employee |
| 12 | join_date | DATE | — | NO | — | — | Date the employee joined the organization |
| 13 | status | VARCHAR | 20 | NO | active | — | Status: active / inactive / on_leave / terminated |
| 14 | profile_picture | VARCHAR | 100 | YES | NULL | — | File path of the employee profile photo |
| 15 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the employee record was created |

---

## 9. `employees_attendance`

**Description:**
Tracks daily attendance of each employee. Records check-in and check-out times
along with the attendance status. Only one record is allowed per employee per day.

**Constraint:** UNIQUE (employee_id, date)

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each attendance record |
| 2 | employee_id | INTEGER | — | NO | — | FK | References employees_employee(id) |
| 3 | date | DATE | — | NO | — | — | Date for which attendance is recorded |
| 4 | status | VARCHAR | 20 | NO | present | — | Status: present / absent / late / half_day / leave |
| 5 | check_in | TIME | — | YES | NULL | — | Time when the employee checked in |
| 6 | check_out | TIME | — | YES | NULL | — | Time when the employee checked out |
| 7 | notes | TEXT | — | YES | NULL | — | Additional remarks about the attendance record |

---

## 10. `employees_leave`

**Description:**
Manages employee leave requests including leave type, duration, reason,
and approval status. Leave applications are reviewed and approved/rejected
by managers or admins.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each leave request |
| 2 | employee_id | INTEGER | — | NO | — | FK | References employees_employee(id) |
| 3 | leave_type | VARCHAR | 20 | NO | casual | — | Type: sick / casual / annual / other |
| 4 | start_date | DATE | — | NO | — | — | Start date of the leave period |
| 5 | end_date | DATE | — | NO | — | — | End date of the leave period |
| 6 | reason | TEXT | — | NO | — | — | Reason provided by the employee for the leave |
| 7 | status | VARCHAR | 20 | NO | pending | — | Approval status: pending / approved / rejected |
| 8 | approved_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) |
| 9 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the leave request was submitted |

---

## 11. `sales_sale`

**Description:**
Stores all sales transaction records (invoices). Each sale captures the customer,
payment method, financial totals, and full audit information for corrections
and voids. This is the primary financial transaction table of the system.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each sale transaction |
| 2 | invoice_number | VARCHAR | 50 | NO | Auto | UNIQUE | Auto-generated invoice number (format: INV-YY-NN) |
| 3 | customer_id | INTEGER | — | YES | NULL | FK | References customers_customer(id) |
| 4 | sale_date | DATETIME | — | NO | Now | — | Date and time when the sale was made |
| 5 | payment_method | VARCHAR | 20 | NO | cash | — | Payment mode: cash / upi / card |
| 6 | status | VARCHAR | 20 | NO | completed | — | Status: completed / corrected / voided / refunded / partial_refund |
| 7 | subtotal | DECIMAL | 12,2 | NO | 0.00 | — | Total before discount and tax |
| 8 | discount_amount | DECIMAL | 10,2 | NO | 0.00 | — | Flat discount amount applied to the sale |
| 9 | discount_percentage | DECIMAL | 5,2 | NO | 0.00 | — | Percentage discount applied to the sale |
| 10 | gst_amount | DECIMAL | 10,2 | NO | 0.00 | — | Total GST or tax amount collected |
| 11 | grand_total | DECIMAL | 12,2 | NO | 0.00 | — | Final payable amount after discount and tax |
| 12 | amount_paid | DECIMAL | 12,2 | NO | 0.00 | — | Actual amount received from the customer |
| 13 | change_amount | DECIMAL | 10,2 | NO | 0.00 | — | Change or balance returned to the customer |
| 14 | notes | TEXT | — | YES | NULL | — | Additional notes or remarks on the sale |
| 15 | created_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — cashier who billed |
| 16 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the invoice was created |
| 17 | void_reason | VARCHAR | 255 | YES | NULL | — | Reason provided when voiding the invoice |
| 18 | voided_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who voided it |
| 19 | voided_at | DATETIME | — | YES | NULL | — | Timestamp when the invoice was voided |
| 20 | correction_reason | VARCHAR | 255 | YES | NULL | — | Reason provided when correcting the invoice |
| 21 | corrected_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who corrected it |
| 22 | corrected_at | DATETIME | — | YES | NULL | — | Timestamp when the invoice was corrected |

---

## 12. `sales_saleitem`

**Description:**
Stores individual product line items within each sale or invoice. Each row
represents one product entry in a transaction. A single sale can have
multiple sale items.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each sale item line |
| 2 | sale_id | INTEGER | — | NO | — | FK | References sales_sale(id) |
| 3 | product_id | INTEGER | — | NO | — | FK | References products_product(id) |
| 4 | quantity | INTEGER | — | NO | — | — | Number of units sold in this line item |
| 5 | unit_price | DECIMAL | 10,2 | NO | — | — | Selling price per unit at the time of sale |
| 6 | discount | DECIMAL | 10,2 | NO | 0.00 | — | Discount amount applied to this specific item |
| 7 | gst_percentage | DECIMAL | 5,2 | NO | 0.00 | — | GST percentage applied to this specific item |
| 8 | total_price | DECIMAL | 12,2 | NO | — | — | Final price for this line (qty × price − discount) |

---

## 13. `sales_invoiceauditlog`

**Description:**
Maintains a complete and tamper-proof audit trail of all actions performed
on every invoice. Used for security, accountability, and tracing invoice history.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each audit log entry |
| 2 | sale_id | INTEGER | — | NO | — | FK | References sales_sale(id) |
| 3 | action | VARCHAR | 30 | NO | — | — | Action: created / corrected / voided / printed / downloaded / refunded |
| 4 | details | TEXT | — | NO | '' | — | Full description of the changes or event |
| 5 | user_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who performed the action |
| 6 | created_at | DATETIME | — | NO | Auto | — | Timestamp when this log entry was recorded |

---

## 14. `purchase_purchaseorder`

**Description:**
Records all purchase orders placed with suppliers to restock inventory.
Tracks the order lifecycle from placement through receipt, and also
tracks payment progress against the total order value.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each purchase order |
| 2 | order_number | VARCHAR | 50 | NO | Auto | UNIQUE | Auto-generated order number (format: PO-YY-NN) |
| 3 | bill_number | VARCHAR | 100 | YES | NULL | — | Supplier's own invoice or bill number |
| 4 | supplier_id | INTEGER | — | NO | — | FK | References suppliers_supplier(id) |
| 5 | order_date | DATE | — | NO | Auto | — | Date when the purchase order was placed |
| 6 | expected_delivery | DATE | — | YES | NULL | — | Expected date when goods will be delivered |
| 7 | status | VARCHAR | 20 | NO | pending | — | Status: pending / received / partial / cancelled |
| 8 | notes | TEXT | — | YES | NULL | — | Additional notes or instructions for the order |
| 9 | total_amount | DECIMAL | 12,2 | NO | 0.00 | — | Total value of all items in the purchase order |
| 10 | paid_amount | DECIMAL | 12,2 | NO | 0.00 | — | Total amount paid to the supplier so far |
| 11 | created_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who created the order |
| 12 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the purchase order was created |
| 13 | updated_at | DATETIME | — | NO | Auto | — | Timestamp when the purchase order was last updated |

---

## 15. `purchase_purchaseitem`

**Description:**
Stores individual product line items within each purchase order. Tracks
both the ordered quantity and the actual received quantity, allowing
partial delivery tracking.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each purchase order item |
| 2 | purchase_order_id | INTEGER | — | NO | — | FK | References purchase_purchaseorder(id) |
| 3 | product_id | INTEGER | — | NO | — | FK | References products_product(id) |
| 4 | quantity | INTEGER | — | NO | — | — | Quantity of the product ordered |
| 5 | purchase_price | DECIMAL | 10,2 | NO | — | — | Price per unit agreed with the supplier |
| 6 | received_quantity | INTEGER | — | NO | 0 | — | Actual quantity received from the supplier |

---

## 16. `purchase_supplierpayment`

**Description:**
Records individual payment transactions made to suppliers against specific
purchase orders. Allows tracking of partial and full payments with
different payment methods.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each supplier payment |
| 2 | purchase_order_id | INTEGER | — | NO | — | FK | References purchase_purchaseorder(id) |
| 3 | amount | DECIMAL | 12,2 | NO | — | — | Payment amount transferred to the supplier |
| 4 | payment_method | VARCHAR | 20 | NO | cash | — | Mode: cash / upi / card / bank / cheque |
| 5 | payment_date | DATE | — | NO | Auto | — | Date when the payment was made |
| 6 | note | TEXT | — | YES | NULL | — | Optional note or transaction reference |
| 7 | created_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who recorded it |

---

## 17. `inventory_stockmovement`

**Description:**
Automatically records every change in product stock quantity, whether caused
by a sale, a purchase receipt, or a manual adjustment. Provides a complete
and chronological history of all stock movements for each product.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each stock movement record |
| 2 | product_id | INTEGER | — | NO | — | FK | References products_product(id) |
| 3 | movement_type | VARCHAR | 20 | NO | — | — | Type: in / out / adjust / damaged / return |
| 4 | quantity | INTEGER | — | NO | — | — | Number of units involved in this movement |
| 5 | quantity_before | INTEGER | — | NO | 0 | — | Stock level before this movement occurred |
| 6 | quantity_after | INTEGER | — | NO | 0 | — | Stock level after this movement occurred |
| 7 | reason | TEXT | — | YES | NULL | — | Reason or explanation for the stock movement |
| 8 | reference | VARCHAR | 100 | YES | NULL | — | Related record reference (Invoice No. or PO No.) |
| 9 | created_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who triggered it |
| 10 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the stock movement was recorded |

---

## 18. `inventory_stockadjustment`

**Description:**
Records manual stock corrections made by authorized users for reasons such
as damage, theft, data entry errors, or returns. On save, it automatically
updates the product stock and creates a corresponding StockMovement record.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each stock adjustment |
| 2 | product_id | INTEGER | — | NO | — | FK | References products_product(id) |
| 3 | adjustment_type | VARCHAR | 10 | NO | — | — | Direction of adjustment: add / reduce |
| 4 | quantity | INTEGER | — | NO | — | — | Number of units to be added or reduced |
| 5 | reason | TEXT | — | NO | — | — | Mandatory reason for making the stock adjustment |
| 6 | created_by_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — who adjusted |
| 7 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the adjustment was recorded |

---

## 19. `notifications_notification`

**Description:**
Stores system-generated notifications sent to users. Notifications are
triggered automatically for events like low stock alerts, completed sales,
purchase order updates, and employee activity.

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | Auto | PK | Unique identifier for each notification |
| 2 | title | VARCHAR | 200 | NO | — | — | Short title or heading of the notification |
| 3 | message | TEXT | — | NO | — | — | Full notification message body |
| 4 | notification_type | VARCHAR | 20 | NO | system | — | Type: low_stock / sale / purchase / employee / system |
| 5 | is_read | BOOLEAN | — | NO | FALSE | — | Whether the user has marked the notification as read |
| 6 | link | VARCHAR | 200 | YES | NULL | — | URL to redirect when the notification is clicked |
| 7 | user_id | INTEGER | — | YES | NULL | FK | References accounts_customuser(id) — target recipient |
| 8 | created_at | DATETIME | — | NO | Auto | — | Timestamp when the notification was generated |

---

## 20. `settings_app_companysettings`

**Description:**
A singleton table that holds company-wide configuration settings. Only one
record (id = 1) is ever stored in this table. These settings control
branding, invoicing, currency, and system-wide defaults across the
entire application.

**Note:** This is a Singleton model — only 1 record is ever inserted (pk = 1 always).

| # | Field Name | Data Type | Size | Null | Default | Key | Description |
|---|------------|-----------|------|------|---------|-----|-------------|
| 1 | id | INTEGER | — | NO | 1 | PK | Always 1 — only one record exists in this table |
| 2 | company_name | VARCHAR | 200 | NO | Fenix IT Mall | — | Official registered name of the company |
| 3 | company_logo | VARCHAR | 100 | YES | NULL | — | File path of the company logo (upload: settings/) |
| 4 | tagline | VARCHAR | 200 | NO | Smart Inventory • Smart Business | — | Company tagline shown on invoices and UI |
| 5 | phone | VARCHAR | 15 | YES | NULL | — | Company contact phone number |
| 6 | email | VARCHAR | 254 | YES | NULL | — | Company contact email address |
| 7 | address | TEXT | — | YES | NULL | — | Company physical or registered address |
| 8 | gst_number | VARCHAR | 20 | YES | NULL | — | Company's GST registration number |
| 9 | invoice_prefix | VARCHAR | 10 | NO | INV | — | Prefix used when generating invoice numbers |
| 10 | currency_symbol | VARCHAR | 5 | NO | ₹ | — | Currency symbol displayed throughout the system |
| 11 | currency_code | VARCHAR | 5 | NO | INR | — | ISO currency code (e.g., INR, USD) |
| 12 | low_stock_threshold | INTEGER | — | NO | 5 | — | Global default minimum stock before alert triggers |
| 13 | theme | VARCHAR | 20 | NO | dark | — | UI theme preference: dark / light |
| 14 | website | VARCHAR | 200 | YES | NULL | — | Company website URL |
| 15 | updated_at | DATETIME | — | NO | Auto | — | Timestamp of the last settings update |

---

## LEGEND

| Symbol / Term | Meaning |
|---------------|---------|
| **PK** | Primary Key — Uniquely identifies each record in the table |
| **FK** | Foreign Key — Links to the Primary Key of another table |
| **FK (1-1)** | One-to-One Foreign Key — Each value can only appear once |
| **UNIQUE** | Value must be unique across all rows in the column |
| **Auto** | Value is automatically generated by the system |
| **NO** | Field is mandatory — cannot be empty (NOT NULL) |
| **YES** | Field is optional — can be empty (NULL allowed) |
| **VARCHAR(n)** | Variable-length text with maximum n characters |
| **TEXT** | Unlimited length text field |
| **INTEGER** | Whole number (no decimals) |
| **DECIMAL(x,y)** | Number with up to x digits total, y digits after decimal |
| **BOOLEAN** | Stores only TRUE or FALSE |
| **DATE** | Stores date only (YYYY-MM-DD) |
| **TIME** | Stores time only (HH:MM:SS) |
| **DATETIME** | Stores both date and time together |

---

*— End of Data Dictionary —*
