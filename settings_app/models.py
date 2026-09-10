"""
Settings App – Models: Singleton company settings
"""
from django.db import models


class CompanySettings(models.Model):
    """Singleton model for company-wide settings"""
    company_name = models.CharField(max_length=200, default='Fenix IT Mall')
    company_logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    tagline = models.CharField(max_length=200, default='Smart Inventory • Smart Business')
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    invoice_prefix = models.CharField(max_length=10, default='INV')
    currency_symbol = models.CharField(max_length=5, default='₹')
    currency_code = models.CharField(max_length=5, default='INR')
    low_stock_threshold = models.IntegerField(default=5)
    theme = models.CharField(max_length=20, default='dark', choices=[('dark', 'Dark'), ('light', 'Light')])
    website = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Settings'
        verbose_name_plural = 'Company Settings'

    @property
    def logo(self):
        return self.company_logo

    def __str__(self):
        return self.company_name


    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton: only one record
        super().save(*args, **kwargs)
