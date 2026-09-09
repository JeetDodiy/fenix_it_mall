"""
Sales App – Models: Sale, SaleItem, InvoiceAuditLog
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
    ]
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('corrected', 'Corrected'),
        ('voided', 'Voided'),
        ('refunded', 'Refunded'),
        ('partial_refund', 'Partial Refund'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    sale_date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')

    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Audit & Tracking
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_sales')
    created_at = models.DateTimeField(auto_now_add=True)

    # Void Tracking
    void_reason = models.CharField(max_length=255, blank=True, null=True)
    voided_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='voided_sales')
    voided_at = models.DateTimeField(null=True, blank=True)

    # Correction Tracking
    correction_reason = models.CharField(max_length=255, blank=True, null=True)
    corrected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='corrected_sales')
    corrected_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year = timezone.now().strftime("%y")
            prefix = f'INV-{year}-'
            existing = Sale.objects.filter(invoice_number__startswith=prefix).values_list('invoice_number', flat=True)
            max_num = 0
            for inv in existing:
                try:
                    num = int(inv.split('-')[-1])
                    if num > max_num:
                        max_num = num
                except (ValueError, IndexError):
                    pass
            self.invoice_number = f'{prefix}{max_num + 1:02d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-created_at']


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'


class InvoiceAuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Invoice Created'),
        ('corrected', 'Invoice Corrected'),
        ('voided', 'Invoice Voided'),
        ('printed', 'Invoice Printed'),
        ('downloaded', 'PDF Downloaded'),
        ('refunded', 'Payment Refunded'),
    ]

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sale.invoice_number} – {self.get_action_display()} ({self.created_at.strftime("%d %b %Y %H:%M")})'
