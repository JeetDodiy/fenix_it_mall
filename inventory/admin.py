from django.contrib import admin
from .models import StockMovement, StockAdjustment


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'quantity_before', 'quantity_after', 'reference', 'created_by', 'created_at')
    list_filter = ('movement_type',)
    search_fields = ('product__name', 'reference')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'adjustment_type', 'quantity', 'reason', 'created_by', 'created_at')
    list_filter = ('adjustment_type',)
    search_fields = ('product__name',)
    readonly_fields = ('created_at',)
