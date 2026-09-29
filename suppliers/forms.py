"""
Suppliers App – Forms
"""
from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_person', 'phone', 'email', 'address', 'gst_number', 'is_active']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Company name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact person name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit number', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter 10-digit phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@company.com'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'gst_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'GST number'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone
