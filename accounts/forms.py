"""
Accounts App – Forms
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser
from core.utils import sanitize_and_process_image


class CustomUserCreationForm(UserCreationForm):
    is_superuser_status = forms.BooleanField(
        required=False,
        label='Grant Super Admin Privileges',
        help_text='Grants full root access including Django Admin and system configuration.',
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

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

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if not (current_user and current_user.is_superuser):
            if 'is_superuser_status' in self.fields:
                del self.fields['is_superuser_status']

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'is_superuser_status' in self.cleaned_data:
            user.is_superuser = self.cleaned_data['is_superuser_status']
            user.is_staff = self.cleaned_data['is_superuser_status']
            if user.is_superuser:
                user.role = 'admin'
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove password field from profile edit
    is_superuser_status = forms.BooleanField(
        required=False,
        label='Grant Super Admin Privileges',
        help_text='Grants full root access including Django Admin and system configuration.',
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    
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

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if current_user and current_user.is_superuser:
            self.fields['is_superuser_status'].initial = self.instance.is_superuser
        else:
            if 'is_superuser_status' in self.fields:
                del self.fields['is_superuser_status']

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'is_superuser_status' in self.cleaned_data:
            user.is_superuser = self.cleaned_data['is_superuser_status']
            user.is_staff = self.cleaned_data['is_superuser_status']
            if user.is_superuser:
                user.role = 'admin'
        if commit:
            user.save()
        return user


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
        phone = (self.cleaned_data.get('phone') or '').strip()
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


class CustomPasswordResetForm(PasswordResetForm):
    """Password reset form: validates email exists in database."""
    email = forms.EmailField(
        label='Email Address',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'login-input',
            'placeholder': 'Enter your registered email',
            'autofocus': True,
        })
    )

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('No account found with this email address.')
        return email
