"""
Settings App – Forms
"""
from django import forms
from .models import CompanySettings


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['company_name', 'company_logo', 'tagline', 'phone', 'email',
                  'address', 'gst_number', 'invoice_prefix', 'currency_symbol',
                  'currency_code', 'low_stock_threshold', 'theme', 'website']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-input'}),
            'tagline': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'gst_number': forms.TextInput(attrs={'class': 'form-input'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-input'}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-input'}),
            'currency_code': forms.TextInput(attrs={'class': 'form-input'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
        }
