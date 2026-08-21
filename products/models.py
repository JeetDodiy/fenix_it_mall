"""
Products App – Models: Category, Brand, Product, ProductImage
"""
import uuid
import os
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def product_count(self):
        return self.products.filter(is_active=True).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ]

    # Core fields
    name = models.CharField(max_length=200)
    product_code = models.CharField(max_length=50, unique=True, blank=True)
    barcode_number = models.CharField(max_length=50, blank=True, null=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # Relations
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    # Pricing
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)

    # Details
    description = models.TextField(blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Stock
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Track if barcode changed
        barcode_changed = False
        if self.pk:
            old = Product.objects.filter(pk=self.pk).first()
            if old and old.barcode_number != self.barcode_number:
                barcode_changed = True
        
        if not self.product_code:
            self.product_code = f'FIM-{str(uuid.uuid4())[:8].upper()}'
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.product_code}')
        if not self.barcode_number:
            self.barcode_number = self.product_code
        
        # If barcode changed, clear old images to regenerate
        if barcode_changed:
            self.barcode_image = None
            self.qr_code = None
        
        super().save(*args, **kwargs)
        self._generate_barcode()
        self._generate_qr()

    def _generate_barcode(self):
        """Generate barcode image using Code128 format"""
        if self.barcode_image or not self.pk:
            return
        try:
            from barcode import Code128
            from barcode.writer import ImageWriter
            
            # Clean barcode number for filename
            safe_barcode = str(self.barcode_number).replace('/', '_').replace('\\', '_')
            
            buf = BytesIO()
            Code128(str(self.barcode_number), writer=ImageWriter()).write(buf)
            buf.seek(0)
            
            filename = f'barcode_{safe_barcode}_{self.pk}.png'
            self.barcode_image.save(filename, ContentFile(buf.read()), save=False)
            Product.objects.filter(pk=self.pk).update(barcode_image=self.barcode_image)
        except Exception as e:
            print(f"Barcode generation error: {e}")
            pass

    def _generate_qr(self):
        """Generate QR code with product information"""
        if self.qr_code or not self.pk:
            return
        try:
            import qrcode
            from PIL import Image
            
            # Clean barcode number for filename
            safe_barcode = str(self.barcode_number).replace('/', '_').replace('\\', '_')
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=2,
            )
            qr_data = f'Product: {self.name}\nCode: {self.product_code}\nBarcode: {self.barcode_number}\nPrice: ₹{self.selling_price}'
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color='black', back_color='white')
            buf = BytesIO()
            img.save(buf, 'PNG')
            buf.seek(0)
            
            filename = f'qr_{safe_barcode}_{self.pk}.png'
            self.qr_code.save(filename, ContentFile(buf.read()), save=False)
            Product.objects.filter(pk=self.pk).update(qr_code=self.qr_code)
        except Exception as e:
            print(f"QR code generation error: {e}")
            pass

    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        return self.stock_quantity <= 0

    @property
    def profit_margin(self):
        if self.purchase_price > 0:
            return ((self.selling_price - self.purchase_price) / self.purchase_price) * 100
        return 0

    @property
    def main_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    def __str__(self):
        return f'{self.name} ({self.product_code})'

    class Meta:
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.product.name}'

    class Meta:
        ordering = ['-is_primary', 'created_at']
