"""Products App – Forms"""
from django import forms
from .models import Product, Category, Brand, ProductImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo', 'description', 'website', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brand name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://'}),
            'logo': forms.FileInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'brand', 'supplier',
            'barcode_number',
            'purchase_price', 'selling_price', 'gst_percentage',
            'stock_quantity', 'low_stock_threshold',
            'warranty', 'description', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product name'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'brand': forms.Select(attrs={'class': 'form-input'}),
            'supplier': forms.Select(attrs={'class': 'form-input'}),
            'barcode_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter barcode number (auto-generated if empty)',
                'id': 'id_barcode_number'
            }),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'gst_percentage': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-input'}),
            'warranty': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '1 Year'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError('Product name is required.')

        # Case-insensitive duplicate check
        qs = Product.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            existing = qs.first()
            raise forms.ValidationError(
                f'A product with the name "{existing.name}" already exists in the inventory (SKU: {existing.product_code}). Duplicate product names are restricted.'
            )
        return name

    def clean_barcode_number(self):
        barcode = (self.cleaned_data.get('barcode_number') or '').strip()
        if barcode:
            qs = Product.objects.filter(barcode_number__iexact=barcode)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                existing = qs.first()
                raise forms.ValidationError(
                    f'Barcode "{barcode}" is already assigned to product "{existing.name}".'
                )
        return barcode




class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class ProductImageForm(forms.Form):
    images = forms.ImageField(
        widget=MultipleFileInput(attrs={'class': 'form-input'}),
        required=False
    )
