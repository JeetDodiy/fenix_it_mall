"""
Management command to purge all QA / test case data from the database.
"""
from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand
from customers.models import Customer
from suppliers.models import Supplier
from employees.models import Employee
from notifications.models import Notification

class Command(BaseCommand):
    help = "Removes all QA test case data from the database."

    def handle(self, *args, **options):
        # 1. Products
        deleted_prods, _ = Product.objects.filter(product_code='QA-TEST-PROD').delete()
        # 2. Categories
        deleted_cats, _ = Category.objects.filter(name='Test Category Auto').delete()
        # 3. Brands
        deleted_brands, _ = Brand.objects.filter(name='Test Brand Auto').delete()
        # 4. Customers
        deleted_custs, _ = Customer.objects.filter(phone='9990001111').delete()
        # 5. Suppliers
        deleted_supps, _ = Supplier.objects.filter(company_name='QA Test Supplier Ltd').delete()
        # 6. Employees
        deleted_emps, _ = Employee.objects.filter(first_name='QA').delete()
        # 7. Notifications
        deleted_notifs, _ = Notification.objects.filter(title__icontains='QA').delete()

        self.stdout.write(self.style.SUCCESS(
            f"Cleaned up test data:\n"
            f"- Products removed: {deleted_prods}\n"
            f"- Categories removed: {deleted_cats}\n"
            f"- Brands removed: {deleted_brands}\n"
            f"- Customers removed: {deleted_custs}\n"
            f"- Suppliers removed: {deleted_supps}\n"
            f"- Employees removed: {deleted_emps}\n"
            f"- Notifications removed: {deleted_notifs}"
        ))
