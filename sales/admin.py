from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'sale_date', 'grand_total', 'payment_method', 'status', 'created_by')
    list_filter = ('status', 'payment_method', 'sale_date')
    search_fields = ('invoice_number', 'customer__name')
    readonly_fields = ('invoice_number', 'created_at')
    inlines = [SaleItemInline]
    date_hierarchy = 'sale_date'


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'total_price')
    search_fields = ('sale__invoice_number', 'product__name')
