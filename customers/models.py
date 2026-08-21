"""
Customers App – Models
"""
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    reward_points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.phone})'

    @property
    def total_purchases(self):
        return self.sales.aggregate(
            total=models.Sum('grand_total')
        )['total'] or 0

    @property
    def total_orders(self):
        return self.sales.count()

    class Meta:
        ordering = ['name']
