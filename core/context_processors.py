"""
Core App – Context Processors
"""
from settings_app.models import CompanySettings
from notifications.models import Notification


def site_settings(request):
    """Make company settings available globally in all templates"""
    try:
        company = CompanySettings.get_settings()
    except Exception:
        company = None
    return {'company_settings': company}


def notifications_processor(request):
    """Make unread notifications count available globally"""
    if request.user.is_authenticated:
        try:
            # Admins / managers see ALL unread notifications (including stock alerts)
            is_privileged = (
                request.user.is_staff
                or request.user.is_superuser
                or getattr(request.user, 'is_manager', False)
            )
            if is_privileged:
                count = Notification.objects.filter(is_read=False).count()
                recent = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
            else:
                count = Notification.objects.filter(user=request.user, is_read=False).count()
                recent = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
        except Exception:
            count = 0
            recent = []
        return {
            'unread_notifications_count': count,
            'recent_notifications': recent,
        }
    return {'unread_notifications_count': 0, 'recent_notifications': []}
