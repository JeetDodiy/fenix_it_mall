"""
Purchase App – Models: PurchaseOrder, PurchaseItem, SupplierPayment
"""
import uuid
from django.db import models
from django.conf import settings


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('partial', 'Partially Received'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True, blank=True)
    bill_number = models.CharField(max_length=100, blank=True, null=True, help_text="Supplier's invoice/bill number")
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateField(auto_now_add=True)
    expected_delivery = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'PO-{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)

    @property
    def balance_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f'{self.order_number} – {self.supplier.company_name}'

    class Meta:
        ordering = ['-created_at']


class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.IntegerField(default=0)

    @property
    def total_price(self):
        return self.quantity * self.purchase_price

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'


class SupplierPayment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    payment_date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Payment ₹{self.amount} for {self.purchase_order.order_number}'
