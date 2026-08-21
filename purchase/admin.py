from django.contrib import admin
from .models import PurchaseOrder, PurchaseItem, SupplierPayment


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


class SupplierPaymentInline(admin.TabularInline):
    model = SupplierPayment
    extra = 0


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'order_date', 'status', 'total_amount', 'paid_amount', 'balance_amount')
    list_filter = ('status',)
    search_fields = ('order_number', 'supplier__company_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [PurchaseItemInline, SupplierPaymentInline]
