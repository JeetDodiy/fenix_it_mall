from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_code', 'category', 'brand', 'purchase_price', 'selling_price', 'stock_quantity', 'status', 'is_active')
    list_filter = ('category', 'brand', 'status', 'is_active')
    search_fields = ('name', 'product_code', 'barcode_number')
    list_editable = ('selling_price', 'stock_quantity', 'status')
    readonly_fields = ('product_code', 'slug', 'created_at', 'updated_at')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'product_code', 'slug', 'category', 'brand', 'supplier', 'description', 'warranty', 'status', 'is_active')}),
        ('Pricing', {'fields': ('purchase_price', 'selling_price', 'gst_percentage')}),
        ('Stock', {'fields': ('stock_quantity', 'low_stock_threshold')}),
        ('Barcode & QR', {'fields': ('barcode_number', 'barcode_image', 'qr_code')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
