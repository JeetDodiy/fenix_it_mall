"""
Management command to safely purge all demo and test data from Fenix IT Mall.
Preserves the superuser 'admin' account and singleton CompanySettings.
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from products.models import Product, Category, Brand, ProductImage
from sales.models import Sale, SaleItem, InvoiceAuditLog
from purchase.models import PurchaseOrder, PurchaseItem, SupplierPayment
from inventory.models import StockMovement, StockAdjustment
from customers.models import Customer
from suppliers.models import Supplier
from employees.models import Employee, Attendance, Leave
from notifications.models import Notification
from settings_app.models import CompanySettings
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Safely deletes all demo/test products, sales, purchases, inventory, suppliers, customers, and test users."

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-categories',
            action='store_true',
            help='Preserve categories instead of deleting them.',
        )
        parser.add_argument(
            '--keep-brands',
            action='store_true',
            help='Preserve brands instead of deleting them.',
        )
        parser.add_argument(
            '--keep-customers',
            action='store_true',
            help='Preserve customers instead of deleting them.',
        )
        parser.add_argument(
            '--keep-suppliers',
            action='store_true',
            help='Preserve suppliers instead of deleting them.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Display records that would be removed without making database modifications.',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        keep_categories = options.get('keep_categories', False)
        keep_brands = options.get('keep_brands', False)
        keep_customers = options.get('keep_customers', False)
        keep_suppliers = options.get('keep_suppliers', False)

        self.stdout.write("=" * 60)
        self.stdout.write(self.style.WARNING("FENIX IT MALL - DEMO DATA CLEANUP ENGINE"))
        self.stdout.write("=" * 60)

        if dry_run:
            self.stdout.write(self.style.NOTICE("DRY RUN MODE: No database changes will be saved.\n"))

        counts = {
            'sale_items': SaleItem.objects.count(),
            'invoice_logs': InvoiceAuditLog.objects.count(),
            'sales': Sale.objects.count(),
            'purchase_items': PurchaseItem.objects.count(),
            'supplier_payments': SupplierPayment.objects.count(),
            'purchase_orders': PurchaseOrder.objects.count(),
            'stock_movements': StockMovement.objects.count(),
            'stock_adjustments': StockAdjustment.objects.count(),
            'product_images': ProductImage.objects.count(),
            'products': Product.objects.count(),
            'categories': 0 if keep_categories else Category.objects.count(),
            'brands': 0 if keep_brands else Brand.objects.count(),
            'customers': 0 if keep_customers else Customer.objects.count(),
            'suppliers': 0 if keep_suppliers else Supplier.objects.count(),
            'attendances': Attendance.objects.count(),
            'leaves': Leave.objects.count(),
            'employees': Employee.objects.count(),
            'notifications': Notification.objects.count(),
            'test_users': CustomUser.objects.exclude(username='admin').count(),
        }

        self.stdout.write("Records targeted for removal:")
        for key, count in counts.items():
            self.stdout.write(f"  • {key.replace('_', ' ').title()}: {count}")

        if dry_run:
            self.stdout.write(self.style.SUCCESS("\n[DRY RUN COMPLETE] Target records scanned successfully."))
            return

        with transaction.atomic():
            # 1. Sales & Invoices
            InvoiceAuditLog.objects.all().delete()
            SaleItem.objects.all().delete()
            Sale.objects.all().delete()

            # 2. Purchases & Supplier Payments
            SupplierPayment.objects.all().delete()
            PurchaseItem.objects.all().delete()
            PurchaseOrder.objects.all().delete()

            # 3. Inventory movements
            StockMovement.objects.all().delete()
            StockAdjustment.objects.all().delete()

            # 4. Products & Images
            ProductImage.objects.all().delete()
            Product.objects.all().delete()

            # 5. Clean up generated media files (barcodes and qrcodes)
            media_root = settings.MEDIA_ROOT
            for folder in ['barcodes', 'qrcodes']:
                folder_path = os.path.join(media_root, folder)
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                        except Exception as e:
                            self.stderr.write(f"Could not remove {file_path}: {e}")

            # 6. Categories & Brands
            if not keep_categories:
                Category.objects.all().delete()

            if not keep_brands:
                Brand.objects.all().delete()

            # 7. Customers & Suppliers
            if not keep_customers:
                Customer.objects.all().delete()

            if not keep_suppliers:
                Supplier.objects.all().delete()

            # 8. Employees & HR
            Attendance.objects.all().delete()
            Leave.objects.all().delete()
            Employee.objects.all().delete()

            # 9. Notifications
            Notification.objects.all().delete()

            # 10. Non-admin test users (keep admin)
            CustomUser.objects.exclude(username='admin').delete()

            # 11. Ensure Company Settings exists
            CompanySettings.get_settings()

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("DEMO DATA CLEANUP COMPLETED SUCCESSFULLY!"))
        self.stdout.write("=" * 60)
        self.stdout.write("Status:")
        self.stdout.write(f"  • Remaining Products: {Product.objects.count()}")
        self.stdout.write(f"  • Remaining Sales: {Sale.objects.count()}")
        self.stdout.write(f"  • Remaining Purchase Orders: {PurchaseOrder.objects.count()}")
        self.stdout.write(f"  • Remaining Customers: {Customer.objects.count()}")
        self.stdout.write(f"  • Remaining Suppliers: {Supplier.objects.count()}")
        self.stdout.write(f"  • Remaining Categories: {Category.objects.count()}")
        self.stdout.write(f"  • Remaining Brands: {Brand.objects.count()}")
        self.stdout.write(f"  • Active Users: {[u.username for u in CustomUser.objects.all()]}")
        self.stdout.write(f"  • Company Settings: {CompanySettings.get_settings().company_name}")
        self.stdout.write("=" * 60)
