"""
Inventory App – Models: Stock Movement & Stock Adjustment
"""
from django.db import models
from django.conf import settings


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjust', 'Stock Adjustment'),
        ('damaged', 'Damaged'),
        ('return', 'Returned'),
    ]

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    quantity_before = models.IntegerField(default=0)
    quantity_after = models.IntegerField(default=0)
    reason = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)  # Purchase/Sale reference
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} – {self.get_movement_type_display()} ({self.quantity})'

    class Meta:
        ordering = ['-created_at']


class StockAdjustment(models.Model):
    """Stock adjustments for corrections, damage, or returns"""
    ADJUSTMENT_TYPES = [
        ('add', 'Add Stock'),
        ('reduce', 'Reduce Stock'),
    ]
    
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='adjustments')
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update product stock
            product = self.product
            quantity_before = product.stock_quantity
            
            if self.adjustment_type == 'add':
                product.stock_quantity += self.quantity
            else:
                product.stock_quantity -= self.quantity
                
            product.save()
            
            # Create stock movement record
            StockMovement.objects.create(
                product=product,
                movement_type='adjust',
                quantity=self.quantity,
                quantity_before=quantity_before,
                quantity_after=product.stock_quantity,
                reason=self.reason,
                reference=f'Adjustment #{self.pk}',
                created_by=self.created_by
            )
    
    def __str__(self):
        return f'{self.product.name} – {self.get_adjustment_type_display()} ({self.quantity})'
    
    class Meta:
        ordering = ['-created_at']
