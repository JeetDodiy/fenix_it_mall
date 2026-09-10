"""
Management command to seed comprehensive, realistic store catalog data:
Categories, Brands, Suppliers, Products, Company Settings, Customers,
and initial sequential transactions.
Ensures the store is NEVER blank on Render deployment or restart.
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Category, Brand, Product
from suppliers.models import Supplier
from customers.models import Customer
from settings_app.models import CompanySettings
from sales.models import Sale, SaleItem
from purchase.models import PurchaseOrder, PurchaseItem, SupplierPayment
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Seeds full IT Mall catalog (Products, Categories, Brands, Suppliers, Settings) so store is never empty."

    def handle(self, *args, **options):
        self.stdout.write("Checking catalog status...")

        # 1. Company Settings
        settings, created = CompanySettings.objects.get_or_create(id=1, defaults={
            'company_name': 'Fenix IT Mall',
            'tagline': 'Smart Inventory • Smart Retail ERP',
            'gst_number': '24SRE22112DC2',
            'invoice_prefix': 'INV',
            'currency_symbol': '₹',
            'currency_code': 'INR',
            'low_stock_threshold': 5,
            'theme': 'dark',
            'address': '101-104, J.P. Tower, Tagore Rd, Rajkot, Gujarat 360002',
            'phone': '+91 93775 09977',
            'email': 'support@fenix-itmall.com',
        })
        if created:
            self.stdout.write(self.style.SUCCESS("[OK] Initialized Company Settings"))

        # 2. Categories
        cats_data = [
            ("Laptops", "laptops", "Gaming & Business High-Performance Laptops"),
            ("Processors", "processors", "Intel & AMD Desktop CPUs"),
            ("Graphics Cards", "graphics-cards", "NVIDIA GeForce & AMD Radeon GPUs"),
            ("Monitors", "monitors", "Ultra-Wide, IPS, and High-Refresh Gaming Displays"),
            ("Storage & RAM", "storage-ram", "High-speed NVMe PCIe 4.0 SSDs & DDR5 Memory"),
            ("Peripherals", "peripherals", "Mechanical Keyboards, Precision Mice & Audio"),
            ("Cabinets & PSUs", "cabinets-psus", "ATX Gaming Cases, Liquid Coolers & Modular Power Supplies"),
            ("Networking", "networking", "Gigabit Routers, Switches, and Mesh Wi-Fi 6 Systems"),
        ]
        cat_objs = {}
        for name, slug, desc in cats_data:
            c, _ = Category.objects.get_or_create(name=name, defaults={'slug': slug, 'description': desc, 'is_active': True})
            cat_objs[name] = c

        # 3. Brands
        brands_data = [
            ("ASUS", "https://asus.com", "Republic of Gamers & TUF Gaming hardware"),
            ("MSI", "https://msi.com", "Micro-Star International Gaming laptops and components"),
            ("HP", "https://hp.com", "HP OMEN & Victus series gaming PCs"),
            ("Dell", "https://dell.com", "Dell XPS, Latitude & Alienware computing systems"),
            ("Intel", "https://intel.com", "Core i9, i7, i5 hybrid desktop processors"),
            ("AMD", "https://amd.com", "Ryzen CPUs and Radeon graphics"),
            ("NVIDIA", "https://nvidia.com", "GeForce RTX graphics solutions"),
            ("Samsung", "https://samsung.com", "PRO Series NVMe Solid State Drives"),
            ("Kingston", "https://kingston.com", "Fury Beast high-frequency DDR5 memory"),
            ("Logitech", "https://logitech.com", "Logitech G and MX series premium peripherals"),
            ("Corsair", "https://corsair.com", "Gaming mechanical keyboards and liquid cooling"),
            ("Ant Esports", "https://antesports.com", "Gaming cabinets and RGB cooling accessories"),
        ]
        brand_objs = {}
        for bname, web, desc in brands_data:
            b, _ = Brand.objects.get_or_create(name=bname, defaults={'website': web, 'description': desc, 'is_active': True})
            brand_objs[bname] = b

        # 4. Suppliers
        supps_data = [
            ("Destiny Computer System", "Jeetu Patel", "9377509977", "destiny@gmail.com", "101-104, J.P. Tower, Tagore Rd, Rajkot, Gujarat", "24DRE12113ZE55"),
            ("Supertron Infotech Ltd", "Rakesh Mehta", "9822011223", "sales@supertron.in", "B-12, Electronics Complex, Ahmedabad, Gujarat", "24AABCS1234F1Z1"),
            ("MSI Enterprise Direct", "Kunal Sharma", "9811445566", "enterprise@msi.com", "Logistics Park, Mumbai, Maharashtra", "27AAECM5566G1Z2"),
            ("TechZone Hardware Distributors", "Amit Verma", "9977881122", "orders@techzone.com", "Ring Road, Surat, Gujarat", "24AABCT9988H1Z3"),
        ]
        supp_objs = {}
        for cname, cperson, phone, email, addr, gst in supps_data:
            s, _ = Supplier.objects.get_or_create(company_name=cname, defaults={
                'contact_person': cperson, 'phone': phone, 'email': email, 'address': addr, 'gst_number': gst, 'is_active': True
            })
            supp_objs[cname] = s

        # 5. Customers
        custs_data = [
            ("Walk-in Retail Customer", "9999999999", "walkin@fenix.local", "In-Store Checkout", 50),
            ("Jeet Dodiya (VIP Client)", "9876543210", "jeet@fenix.local", "Rajkot, Gujarat", 350),
            ("Rahul Sharma", "9822334455", "rahul.sharma@gmail.com", "Ahmedabad", 120),
            ("Priya Patel", "9811223344", "priya.patel@outlook.com", "Surat", 200),
        ]
        cust_objs = []
        for cname, phone, email, addr, pts in custs_data:
            c, _ = Customer.objects.get_or_create(phone=phone, defaults={
                'name': cname, 'email': email, 'address': addr, 'reward_points': pts, 'is_active': True
            })
            cust_objs.append(c)

        # 6. Rich Hardware Products
        products_data = [
            {
                'name': 'ASUS ROG Strix G16 (2025) Core i9-14900HX, RTX 4070',
                'code': 'FIM-ROG16',
                'barcode': '8901234001011',
                'cat': 'Laptops',
                'brand': 'ASUS',
                'supp': 'Destiny Computer System',
                'purchase': Decimal('125000.00'),
                'selling': Decimal('145000.00'),
                'stock': 8,
                'min_stock': 2,
            },
            {
                'name': 'MSI Stealth 14 AI Studio Core Ultra 9, 32GB, 1TB SSD',
                'code': 'FIM-MSI14AI',
                'barcode': '8901234001028',
                'cat': 'Laptops',
                'brand': 'MSI',
                'supp': 'MSI Enterprise Direct',
                'purchase': Decimal('155000.00'),
                'selling': Decimal('180000.00'),
                'stock': 6,
                'min_stock': 2,
            },
            {
                'name': 'HP Victus Gaming Laptop, AMD Ryzen 7 7840HS, 6GB RTX 4050',
                'code': 'FIM-VICTUS7',
                'barcode': '8901234001035',
                'cat': 'Laptops',
                'brand': 'HP',
                'supp': 'Supertron Infotech Ltd',
                'purchase': Decimal('68000.00'),
                'selling': Decimal('78500.00'),
                'stock': 12,
                'min_stock': 3,
            },
            {
                'name': 'Dell Latitude 5440 Core i7-1365U, 16GB RAM, 512GB NVMe',
                'code': 'FIM-DELL5440',
                'barcode': '8901234001042',
                'cat': 'Laptops',
                'brand': 'Dell',
                'supp': 'TechZone Hardware Distributors',
                'purchase': Decimal('56000.00'),
                'selling': Decimal('65000.00'),
                'stock': 10,
                'min_stock': 2,
            },
            {
                'name': 'Intel Core i7-14700K 20-Core Unlocked Desktop Processor',
                'code': 'FIM-I714700K',
                'barcode': '8901234001059',
                'cat': 'Processors',
                'brand': 'Intel',
                'supp': 'Destiny Computer System',
                'purchase': Decimal('32000.00'),
                'selling': Decimal('38500.00'),
                'stock': 15,
                'min_stock': 4,
            },
            {
                'name': 'AMD Ryzen 7 7800X3D 8-Core 16-Thread Gaming Processor',
                'code': 'FIM-RYZEN7800X',
                'barcode': '8901234001066',
                'cat': 'Processors',
                'brand': 'AMD',
                'supp': 'Supertron Infotech Ltd',
                'purchase': Decimal('31000.00'),
                'selling': Decimal('36000.00'),
                'stock': 14,
                'min_stock': 3,
            },
            {
                'name': 'ASUS TUF Gaming GeForce RTX 4070 Ti Super 16GB OC Edition',
                'code': 'FIM-RTX4070TIS',
                'barcode': '8901234001073',
                'cat': 'Graphics Cards',
                'brand': 'ASUS',
                'supp': 'Destiny Computer System',
                'purchase': Decimal('72000.00'),
                'selling': Decimal('82500.00'),
                'stock': 5,
                'min_stock': 2,
            },
            {
                'name': 'MSI GeForce RTX 4060 Ventus 2X Black 8GB GDDR6',
                'code': 'FIM-RTX4060MSI',
                'barcode': '8901234001080',
                'cat': 'Graphics Cards',
                'brand': 'MSI',
                'supp': 'MSI Enterprise Direct',
                'purchase': Decimal('24500.00'),
                'selling': Decimal('28500.00'),
                'stock': 16,
                'min_stock': 4,
            },
            {
                'name': 'Samsung 990 PRO 1TB PCIe Gen4 NVMe M.2 SSD (7450 MB/s)',
                'code': 'FIM-SAM990P1T',
                'barcode': '8901234001097',
                'cat': 'Storage & RAM',
                'brand': 'Samsung',
                'supp': 'Supertron Infotech Ltd',
                'purchase': Decimal('7800.00'),
                'selling': Decimal('9500.00'),
                'stock': 25,
                'min_stock': 5,
            },
            {
                'name': 'Kingston Fury Beast 16GB (1x16GB) 5600MHz DDR5 Desktop RAM',
                'code': 'FIM-KFURY16D5',
                'barcode': '8901234001103',
                'cat': 'Storage & RAM',
                'brand': 'Kingston',
                'supp': 'TechZone Hardware Distributors',
                'purchase': Decimal('3800.00'),
                'selling': Decimal('4800.00'),
                'stock': 30,
                'min_stock': 6,
            },
            {
                'name': 'Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz CL36',
                'code': 'FIM-CORS32D5',
                'barcode': '8901234001110',
                'cat': 'Storage & RAM',
                'brand': 'Corsair',
                'supp': 'Supertron Infotech Ltd',
                'purchase': Decimal('7500.00'),
                'selling': Decimal('9200.00'),
                'stock': 18,
                'min_stock': 4,
            },
            {
                'name': 'Dell UltraSharp U2723QE 27-inch 4K UHD IPS USB-C Monitor',
                'code': 'FIM-DELL27U4K',
                'barcode': '8901234001127',
                'cat': 'Monitors',
                'brand': 'Dell',
                'supp': 'Destiny Computer System',
                'purchase': Decimal('28000.00'),
                'selling': Decimal('34000.00'),
                'stock': 7,
                'min_stock': 2,
            },
            {
                'name': 'ASUS TUF Gaming VG249Q1A 24-inch FHD 165Hz IPS Gaming Monitor',
                'code': 'FIM-ASUS24165',
                'barcode': '8901234001134',
                'cat': 'Monitors',
                'brand': 'ASUS',
                'supp': 'TechZone Hardware Distributors',
                'purchase': Decimal('11500.00'),
                'selling': Decimal('14500.00'),
                'stock': 15,
                'min_stock': 3,
            },
            {
                'name': 'Logitech MX Master 3S Wireless Performance Mouse',
                'code': 'FIM-LOGIMX3S',
                'barcode': '8901234001141',
                'cat': 'Peripherals',
                'brand': 'Logitech',
                'supp': 'Destiny Computer System',
                'purchase': Decimal('7200.00'),
                'selling': Decimal('8995.00'),
                'stock': 20,
                'min_stock': 4,
            },
            {
                'name': 'Corsair K70 RGB PRO Mechanical Gaming Keyboard (Cherry MX)',
                'code': 'FIM-CORSK70',
                'barcode': '8901234001158',
                'cat': 'Peripherals',
                'brand': 'Corsair',
                'supp': 'Supertron Infotech Ltd',
                'purchase': Decimal('9200.00'),
                'selling': Decimal('11500.00'),
                'stock': 12,
                'min_stock': 3,
            },
            {
                'name': 'Ant Esports Crystal X7 ATX Computer Case/Gaming Cabinet',
                'code': 'FIM-ANTX7CAB',
                'barcode': '8901234001165',
                'cat': 'Cabinets & PSUs',
                'brand': 'Ant Esports',
                'supp': 'TechZone Hardware Distributors',
                'purchase': Decimal('4000.00'),
                'selling': Decimal('5200.00'),
                'stock': 14,
                'min_stock': 3,
            },
        ]

        created_prod_count = 0
        for p in products_data:
            existing = Product.objects.filter(name__iexact=p['name']).first()
            if not existing:
                Product.objects.create(
                    name=p['name'],
                    product_code=p['code'],
                    barcode_number=p['barcode'],
                    category=cat_objs.get(p['cat']),
                    brand=brand_objs.get(p['brand']),
                    supplier=supp_objs.get(p['supp']),
                    purchase_price=p['purchase'],
                    selling_price=p['selling'],
                    gst_percentage=Decimal('18.00'),
                    stock_quantity=p['stock'],
                    low_stock_threshold=p['min_stock'],
                    is_active=True,
                )
                created_prod_count += 1

        self.stdout.write(self.style.SUCCESS(f"[OK] Provisioned {created_prod_count} high-performance IT hardware products."))

        # 7. Demo Initial Sales (If none exist)
        admin_user = CustomUser.objects.filter(username='admin').first()
        if admin_user and Sale.objects.count() == 0:
            p1 = Product.objects.first()
            p2 = Product.objects.last()
            if p1 and p2:
                # Sale 1
                s1 = Sale.objects.create(
                    invoice_number='INV-26-01',
                    customer=cust_objs[0],
                    created_by=admin_user,
                    subtotal=p1.selling_price,
                    discount_amount=Decimal('0.00'),
                    gst_amount=(p1.selling_price * Decimal('0.18')).quantize(Decimal('0.01')),
                    grand_total=(p1.selling_price * Decimal('1.18')).quantize(Decimal('0.01')),
                    amount_paid=(p1.selling_price * Decimal('1.18')).quantize(Decimal('0.01')),
                    change_amount=Decimal('0.00'),
                    payment_method='CASH',
                    status='COMPLETED',
                )
                SaleItem.objects.create(
                    sale=s1,
                    product=p1,
                    quantity=1,
                    unit_price=p1.selling_price,
                    total_price=p1.selling_price,
                )

                # Sale 2
                sub2 = p2.selling_price * 2
                s2 = Sale.objects.create(
                    invoice_number='INV-26-02',
                    customer=cust_objs[1],
                    created_by=admin_user,
                    subtotal=sub2,
                    discount_amount=Decimal('500.00'),
                    gst_amount=((sub2 - Decimal('500.00')) * Decimal('0.18')).quantize(Decimal('0.01')),
                    grand_total=((sub2 - Decimal('500.00')) * Decimal('1.18')).quantize(Decimal('0.01')),
                    amount_paid=((sub2 - Decimal('500.00')) * Decimal('1.18')).quantize(Decimal('0.01')),
                    change_amount=Decimal('0.00'),
                    payment_method='UPI',
                    status='COMPLETED',
                )
                SaleItem.objects.create(
                    sale=s2,
                    product=p2,
                    quantity=2,
                    unit_price=p2.selling_price,
                    total_price=sub2,
                )
                self.stdout.write(self.style.SUCCESS("[OK] Seeded initial sales transactions (INV-26-01, INV-26-02)."))

        # 8. Demo Initial Purchase Orders (If none exist)
        if admin_user and PurchaseOrder.objects.count() == 0:
            supp = Supplier.objects.first()
            prod = Product.objects.first()
            if supp and prod:
                po_total = prod.purchase_price * 5
                po = PurchaseOrder.objects.create(
                    order_number='PO-26-01',
                    bill_number='BILL-8821',
                    supplier=supp,
                    created_by=admin_user,
                    order_date=timezone.now().date(),
                    total_amount=po_total,
                    paid_amount=po_total,
                    status='received',
                )
                PurchaseItem.objects.create(
                    purchase_order=po,
                    product=prod,
                    quantity=5,
                    purchase_price=prod.purchase_price,
                    received_quantity=5,
                )
                SupplierPayment.objects.create(
                    purchase_order=po,
                    amount=po_total,
                    payment_date=timezone.now().date(),
                    payment_method='bank',
                    note='Initial stock delivery settlement',
                )
                self.stdout.write(self.style.SUCCESS("[OK] Seeded initial purchase order (PO-26-01)."))

        total_prods = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(f"[SUCCESS] Catalog verification complete! Total products ready in store: {total_prods}"))
