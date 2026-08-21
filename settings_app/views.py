"""
Settings App – Views
"""
import os
import shutil
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from .models import CompanySettings
from .forms import CompanySettingsForm


@login_required
def settings_view(request):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied. Admin only.')
        return redirect('dashboard:index')

    company_settings = CompanySettings.get_settings()
    form = CompanySettingsForm(request.POST or None, request.FILES or None, instance=company_settings)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Settings saved successfully.')
        return redirect('settings_app:settings')

    return render(request, 'settings_app/settings.html', {
        'form': form,
        'company_settings': company_settings,
    })


@login_required
def backup_database(request):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied. Admin only.')
        return redirect('dashboard:index')

    db_path = settings.DATABASES['default']['NAME']
    if not os.path.exists(db_path):
        messages.error(request, 'Database file not found.')
        return redirect('settings_app:settings')

    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f'fenix_backup_{timestamp}.sqlite3'

    with open(db_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
