"""
Purchase App – Forms
"""
from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseItem, SupplierPayment
from suppliers.models import Supplier
from products.models import Product


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'bill_number', 'expected_delivery', 'status', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'bill_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., INV-2026-001'}),
            'expected_delivery': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True)


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'purchase_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True)


PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder, 
    PurchaseItem,
    form=PurchaseItemForm,
    extra=3,
    can_delete=True
)


class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayment
        fields = ['purchase_order', 'amount', 'payment_method', 'note']
        widgets = {
            'purchase_order': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
