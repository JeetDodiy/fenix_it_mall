# 🗄️ Fenix IT Mall — Full Database Table Structure

> **13 apps** · **17 models** · **SQLite** backend

---

## 📦 App Overview

| App | Models |
|-----|--------|
| `accounts` | CustomUser |
| `products` | Category, Brand, Product, ProductImage |
| `customers` | Customer |
| `suppliers` | Supplier |
| `employees` | Employee, Attendance, Leave |
| `sales` | Sale, SaleItem, InvoiceAuditLog |
| `purchase` | PurchaseOrder, PurchaseItem, SupplierPayment |
| `inventory` | StockMovement, StockAdjustment |
| `notifications` | Notification |
| `settings_app` | CompanySettings |
| `core` | *(no models)* |
| `reports` | *(no models)* |
| `dashboard` | *(no models)* |

---

## 🔐 accounts — `CustomUser`
> Extends Django's `AbstractUser` with role-based access.

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `username` | CharField | Unique (inherited) |
| `first_name` | CharField | (inherited) |
| `last_name` | CharField | (inherited) |
| `email` | EmailField | (inherited) |
| `password` | CharField | (inherited) |
| `is_staff` | BooleanField | (inherited) |
| `is_superuser` | BooleanField | (inherited) |
| `role` | CharField(20) | Choices: admin, manager, employee, cashier · Default: employee |
| `phone` | CharField(15) | Nullable |
| `address` | TextField | Nullable |
| `profile_picture` | ImageField | Upload: `profiles/` · Nullable |
| `is_active` | BooleanField | Default: True |
| `created_at` | DateTimeField | Auto on create |
| `updated_at` | DateTimeField | Auto on update |

---

## 📂 products — `Category`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `name` | CharField(100) | Unique |
| `slug` | SlugField(100) | Unique · Auto-generated |
| `image` | ImageField | Upload: `categories/` · Nullable |
| `description` | TextField | Nullable |
| `is_active` | BooleanField | Default: True |
| `created_at` | DateTimeField | Auto on create |

---

## 🏷️ products — `Brand`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `name` | CharField(100) | Unique |
| `logo` | ImageField | Upload: `brands/` · Nullable |
| `description` | TextField | Nullable |
| `website` | URLField | Nullable |
| `is_active` | BooleanField | Default: True |
| `created_at` | DateTimeField | Auto on create |

---

## 📦 products — `Product`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `name` | CharField(200) | Unique |
| `product_code` | CharField(50) | Unique · Auto-gen: `FIM-XXXXXXXX` |
| `barcode_number` | CharField(50) | Nullable |
| `barcode_image` | ImageField | Upload: `barcodes/` · Auto-gen |
| `qr_code` | ImageField | Upload: `qrcodes/` · Auto-gen |
| `slug` | SlugField(200) | Unique · Auto-generated |
| `category_id` | FK → Category | SET_NULL · Nullable |
| `brand_id` | FK → Brand | SET_NULL · Nullable |
| `supplier_id` | FK → Supplier | SET_NULL · Nullable |
| `purchase_price` | DecimalField(10,2) | Default: 0 |
| `selling_price` | DecimalField(10,2) | Default: 0 |
| `gst_percentage` | DecimalField(5,2) | Default: 18.00 |
| `description` | TextField | Nullable |
| `warranty` | CharField(100) | Nullable |
| `status` | CharField(20) | Choices: active, inactive, discontinued |
| `stock_quantity` | IntegerField | Default: 0 |
| `low_stock_threshold` | IntegerField | Default: 5 |
| `is_active` | BooleanField | Default: True |
| `created_at` | DateTimeField | Auto on create |
| `updated_at` | DateTimeField | Auto on update |

---

## 🖼️ products — `ProductImage`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `product_id` | FK → Product | CASCADE |
| `image` | ImageField | Upload: `products/` |
| `is_primary` | BooleanField | Default: False |
| `created_at` | DateTimeField | Auto on create |

---

## 👤 customers — `Customer`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `name` | CharField(200) | |
| `phone` | CharField(15) | Unique |
| `email` | EmailField | Nullable |
| `address` | TextField | Nullable |
| `reward_points` | IntegerField | Default: 0 |
| `is_active` | BooleanField | Default: True |
| `created_at` | DateTimeField | Auto on create |
| `updated_at` | DateTimeField | Auto on update |

---

## 🏢 suppliers — `Supplier`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `company_name` | CharField(200) | |
| `contact_person` | CharField(100) | |
| `phone` | CharField(15) | |
| `email` | EmailField | Nullable |
| `address` | TextField | Nullable |
| `gst_number` | CharField(20) | Nullable |
| `is_active` | BooleanField | Default: True |
| `created_at` | DateTimeField | Auto on create |
| `updated_at` | DateTimeField | Auto on update |

---

## 👷 employees — `Employee`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `user_id` | OneToOne → CustomUser | CASCADE · Nullable |
| `employee_id` | CharField(20) | Unique · Auto-gen: `EMP-XXXXXX` |
| `first_name` | CharField(100) | |
| `last_name` | CharField(100) | |
| `email` | EmailField | Nullable |
| `phone` | CharField(15) | |
| `address` | TextField | Nullable |
| `designation` | CharField(100) | |
| `department` | CharField(100) | Nullable |
| `salary` | DecimalField(10,2) | Default: 0 |
| `join_date` | DateField | |
| `status` | CharField(20) | Choices: active, inactive, on_leave, terminated |
| `profile_picture` | ImageField | Upload: `employees/` · Nullable |
| `created_at` | DateTimeField | Auto on create |

---

## 📅 employees — `Attendance`
> `unique_together`: (employee, date)

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `employee_id` | FK → Employee | CASCADE |
| `date` | DateField | |
| `status` | CharField(20) | Choices: present, absent, late, half_day, leave |
| `check_in` | TimeField | Nullable |
| `check_out` | TimeField | Nullable |
| `notes` | TextField | Nullable |

---

## 🏖️ employees — `Leave`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `employee_id` | FK → Employee | CASCADE |
| `leave_type` | CharField(20) | Choices: sick, casual, annual, other |
| `start_date` | DateField | |
| `end_date` | DateField | |
| `reason` | TextField | |
| `status` | CharField(20) | Choices: pending, approved, rejected |
| `approved_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `created_at` | DateTimeField | Auto on create |

---

## 🧾 sales — `Sale`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `invoice_number` | CharField(50) | Unique · Auto-gen: `INV-YY-NN` |
| `customer_id` | FK → Customer | SET_NULL · Nullable |
| `sale_date` | DateTimeField | Default: now |
| `payment_method` | CharField(20) | Choices: cash, upi, card |
| `status` | CharField(20) | Choices: completed, corrected, voided, refunded, partial_refund |
| `subtotal` | DecimalField(12,2) | Default: 0 |
| `discount_amount` | DecimalField(10,2) | Default: 0 |
| `discount_percentage` | DecimalField(5,2) | Default: 0 |
| `gst_amount` | DecimalField(10,2) | Default: 0 |
| `grand_total` | DecimalField(12,2) | Default: 0 |
| `amount_paid` | DecimalField(12,2) | Default: 0 |
| `change_amount` | DecimalField(10,2) | Default: 0 |
| `notes` | TextField | Nullable |
| `created_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `created_at` | DateTimeField | Auto on create |
| `void_reason` | CharField(255) | Nullable |
| `voided_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `voided_at` | DateTimeField | Nullable |
| `correction_reason` | CharField(255) | Nullable |
| `corrected_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `corrected_at` | DateTimeField | Nullable |

---

## 🛒 sales — `SaleItem`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `sale_id` | FK → Sale | CASCADE |
| `product_id` | FK → Product | CASCADE |
| `quantity` | IntegerField | |
| `unit_price` | DecimalField(10,2) | |
| `discount` | DecimalField(10,2) | Default: 0 |
| `gst_percentage` | DecimalField(5,2) | Default: 0 |
| `total_price` | DecimalField(12,2) | |

---

## 📋 sales — `InvoiceAuditLog`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `sale_id` | FK → Sale | CASCADE |
| `action` | CharField(30) | Choices: created, corrected, voided, printed, downloaded, refunded |
| `details` | TextField | |
| `user_id` | FK → CustomUser | SET_NULL · Nullable |
| `created_at` | DateTimeField | Auto on create |

---

## 📋 purchase — `PurchaseOrder`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `order_number` | CharField(50) | Unique · Auto-gen: `PO-YY-NN` |
| `bill_number` | CharField(100) | Nullable (Supplier's invoice) |
| `supplier_id` | FK → Supplier | CASCADE |
| `order_date` | DateField | Auto on create |
| `expected_delivery` | DateField | Nullable |
| `status` | CharField(20) | Choices: pending, received, partial, cancelled |
| `notes` | TextField | Nullable |
| `total_amount` | DecimalField(12,2) | Default: 0 |
| `paid_amount` | DecimalField(12,2) | Default: 0 |
| `created_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `created_at` | DateTimeField | Auto on create |
| `updated_at` | DateTimeField | Auto on update |

---

## 📦 purchase — `PurchaseItem`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `purchase_order_id` | FK → PurchaseOrder | CASCADE |
| `product_id` | FK → Product | CASCADE |
| `quantity` | IntegerField | |
| `purchase_price` | DecimalField(10,2) | |
| `received_quantity` | IntegerField | Default: 0 |

---

## 💳 purchase — `SupplierPayment`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `purchase_order_id` | FK → PurchaseOrder | CASCADE |
| `amount` | DecimalField(12,2) | |
| `payment_method` | CharField(20) | Choices: cash, upi, card, bank, cheque |
| `payment_date` | DateField | Auto on create |
| `note` | TextField | Nullable |
| `created_by_id` | FK → CustomUser | SET_NULL · Nullable |

---

## 📊 inventory — `StockMovement`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `product_id` | FK → Product | CASCADE |
| `movement_type` | CharField(20) | Choices: in, out, adjust, damaged, return |
| `quantity` | IntegerField | |
| `quantity_before` | IntegerField | Default: 0 |
| `quantity_after` | IntegerField | Default: 0 |
| `reason` | TextField | Nullable |
| `reference` | CharField(100) | Nullable (Purchase/Sale ref) |
| `created_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `created_at` | DateTimeField | Auto on create |

---

## 🔧 inventory — `StockAdjustment`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `product_id` | FK → Product | CASCADE |
| `adjustment_type` | CharField(10) | Choices: add, reduce |
| `quantity` | IntegerField | |
| `reason` | TextField | |
| `created_by_id` | FK → CustomUser | SET_NULL · Nullable |
| `created_at` | DateTimeField | Auto on create |

> 💡 On save, automatically updates `Product.stock_quantity` and creates a `StockMovement` record.

---

## 🔔 notifications — `Notification`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK |
| `title` | CharField(200) | |
| `message` | TextField | |
| `notification_type` | CharField(20) | Choices: low_stock, sale, purchase, employee, system |
| `is_read` | BooleanField | Default: False |
| `link` | CharField(200) | Nullable |
| `user_id` | FK → CustomUser | CASCADE · Nullable |
| `created_at` | DateTimeField | Auto on create |

---

## ⚙️ settings_app — `CompanySettings`
> **Singleton model** — only 1 record (pk=1 always).

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | AutoField | PK (always 1) |
| `company_name` | CharField(200) | Default: 'Fenix IT Mall' |
| `company_logo` | ImageField | Upload: `settings/` · Nullable |
| `tagline` | CharField(200) | Default: 'Smart Inventory • Smart Business' |
| `phone` | CharField(15) | Nullable |
| `email` | EmailField | Nullable |
| `address` | TextField | Nullable |
| `gst_number` | CharField(20) | Nullable |
| `invoice_prefix` | CharField(10) | Default: 'INV' |
| `currency_symbol` | CharField(5) | Default: '₹' |
| `currency_code` | CharField(5) | Default: 'INR' |
| `low_stock_threshold` | IntegerField | Default: 5 |
| `theme` | CharField(20) | Choices: dark, light · Default: dark |
| `website` | URLField | Nullable |
| `updated_at` | DateTimeField | Auto on update |

---

## 🔗 Relationship Diagram

```
CustomUser ──────────────────────────────────────────┐
     │ (OneToOne)                                     │
  Employee ──── Attendance                            │
     │                                                │
     └──── Leave ──── (approved_by) ──► CustomUser    │
                                                      │
Supplier ──── Product ──── Category                  │
    │              │                                  │
PurchaseOrder      └──── Brand                       │
    │              │                                  │
PurchaseItem       └──── ProductImage                │
    │              │                                  │
SupplierPayment    ├──── StockMovement               │
                   └──── StockAdjustment             │
                                                      │
Customer ──── Sale ──── SaleItem ──► Product         │
               │                                      │
               └──── InvoiceAuditLog ──► CustomUser ◄─┘
                                                      
Notification ──► CustomUser                          
CompanySettings (singleton)                          
```
