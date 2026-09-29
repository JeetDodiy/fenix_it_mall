"""
Customers App – Forms
"""
from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'reward_points', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Customer name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit number', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter 10-digit phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'customer@email.com'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'reward_points': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone
