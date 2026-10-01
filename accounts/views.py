"""
Accounts App – Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, CustomPasswordResetForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        
    # Make all form inputs use the form-input class
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-input'
        
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard:index')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = UserProfileForm(instance=request.user)
        
    return render(request, 'accounts/profile.html', {'form': form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    # Add form-input class
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-input'
        
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def user_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')
        
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_add(request):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('accounts:user_list')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Add New User'})


@login_required
def user_edit(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')
        
    user_obj = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('accounts:user_list')
    else:
        form = CustomUserChangeForm(instance=user_obj)
        
    return render(request, 'accounts/user_form.html', {'form': form, 'title': f'Edit User: {user_obj.username}', 'user_obj': user_obj})


@login_required
def admin_change_user_password(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')
    
    user_obj = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not new_password or not confirm_password:
            messages.error(request, 'Both password fields are required.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, f'Password for {user_obj.username} has been changed successfully.')
            return redirect('accounts:user_edit', pk=pk)
    
    return render(request, 'accounts/admin_change_password.html', {'user_obj': user_obj})


@login_required
def user_delete(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    user_obj = get_object_or_404(CustomUser, pk=pk)

    # Safety: cannot delete yourself
    if user_obj.pk == request.user.pk:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('accounts:user_list')

    # Safety: cannot delete last admin
    if user_obj.role == 'admin' and CustomUser.objects.filter(role='admin').count() <= 1:
        messages.error(request, 'Cannot delete the last admin account.')
        return redirect('accounts:user_list')

    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f'User "{username}" has been permanently deleted.')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_delete_confirm.html', {'user_obj': user_obj})


# ── PASSWORD RESET VIEWS ──

class FenixPasswordResetView(PasswordResetView):
    """Step 1: User enters email → sends reset link."""
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class FenixPasswordResetDoneView(PasswordResetDoneView):
    """Step 2: Confirmation that email was sent."""
    template_name = 'accounts/password_reset_done.html'


class FenixPasswordResetConfirmView(PasswordResetConfirmView):
    """Step 3: User clicks link in email → sets new password."""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class FenixPasswordResetCompleteView(PasswordResetCompleteView):
    """Step 4: Password changed successfully."""
    template_name = 'accounts/password_reset_complete.html'
