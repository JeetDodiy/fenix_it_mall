"""
Accounts App – Forms
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from core.utils import sanitize_and_process_image


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'profile_picture')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit number', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter 10-digit phone number'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone


class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove password field from profile edit
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'role', 'profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit number', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter 10-digit phone number'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone


class UserProfileForm(forms.ModelForm):
    """Form for personal profile editing by any user (role is not editable here)"""
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit number', 'maxlength': '10', 'minlength': '10', 'pattern': '[0-9]{10}', 'title': 'Enter 10-digit phone number'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone


    def clean_profile_picture(self):
        pic = self.cleaned_data.get("profile_picture")
        if pic and hasattr(pic, "file"):
            try:
                return sanitize_and_process_image(pic)
            except Exception as e:
                raise forms.ValidationError(f"Invalid image file: {e}")
        return pic
