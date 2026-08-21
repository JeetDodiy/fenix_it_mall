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
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91 1234567890'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'customer@email.com'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'reward_points': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
