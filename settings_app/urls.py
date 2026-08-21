"""Settings App – URLs"""
from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('backup/', views.backup_database, name='backup'),
]
