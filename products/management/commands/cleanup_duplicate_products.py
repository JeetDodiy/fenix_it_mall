"""
Management command to detect and safely deduplicate any duplicate product names.
"""
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Finds and resolves duplicate product names."

    def handle(self, *args, **options):
        all_products = Product.objects.all().order_by('id')
        seen = {}
        duplicates_count = 0

        for p in all_products:
            normalized = p.name.strip().lower()
            if normalized in seen:
                primary = seen[normalized]
                duplicates_count += 1
                self.stdout.write(self.style.WARNING(
                    f"Duplicate found: ID {p.id} '{p.name}' (SKU {p.product_code}) matches ID {primary.id} (SKU {primary.product_code})"
                ))
                
                has_sales = hasattr(p, 'sale_items') and p.sale_items.exists()
                has_po = hasattr(p, 'po_items') and p.po_items.exists()

                if not has_sales and not has_po and p.stock_quantity == 0:
                    self.stdout.write(self.style.SUCCESS(f"Deleting unused 0-stock duplicate product: ID {p.id}"))
                    p.delete()
                else:
                    p.name = f"{p.name.strip()} ({p.product_code})"
                    p.save()
                    self.stdout.write(self.style.NOTICE(f"Renamed duplicate product to distinct name: '{p.name}'"))
            else:
                seen[normalized] = p

        if duplicates_count == 0:
            self.stdout.write(self.style.SUCCESS("No duplicate product names found."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Resolved {duplicates_count} duplicate product(s)."))
