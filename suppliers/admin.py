from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'phone', 'email', 'gst_number', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('company_name', 'contact_person', 'phone', 'email')
    list_editable = ('is_active',)
