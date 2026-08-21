"""
Notifications App – Views
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Notification


@login_required
def notification_list(request):
    # Admins / managers see all notifications; others see only their own
    is_privileged = (
        request.user.is_staff
        or request.user.is_superuser
        or getattr(request.user, 'is_manager', False)
    )
    if is_privileged:
        notifications = Notification.objects.all().order_by('-created_at')
    else:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(notifications, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'notifications/list.html', {'notifications': page})


@login_required
def mark_read(request, pk):
    is_privileged = request.user.is_staff or request.user.is_superuser
    qs = Notification.objects.filter(pk=pk) if is_privileged else Notification.objects.filter(pk=pk, user=request.user)
    notif = qs.first()
    if notif is None:
        return redirect('notifications:list')
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('notifications:list')


@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')


@login_required
def delete_notification(request, pk):
    is_privileged = request.user.is_staff or request.user.is_superuser
    qs = Notification.objects.filter(pk=pk) if is_privileged else Notification.objects.filter(pk=pk, user=request.user)
    notif = qs.first()
    if notif is None:
        return redirect('notifications:list')
    if request.method == 'POST':
        notif.delete()
    return redirect('notifications:list')
