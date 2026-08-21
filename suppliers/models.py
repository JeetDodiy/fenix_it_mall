"""
Suppliers App – Models
"""
from django.db import models


class Supplier(models.Model):
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    @property
    def total_purchases(self):
        return self.purchase_orders.aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0

    class Meta:
        ordering = ['company_name']
