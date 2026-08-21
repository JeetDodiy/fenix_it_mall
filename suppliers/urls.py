"""Suppliers App – URLs"""
from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.supplier_list, name='list'),
    path('add/', views.supplier_add, name='add'),
    path('<int:pk>/', views.supplier_detail, name='detail'),
    path('<int:pk>/edit/', views.supplier_edit, name='edit'),
    path('<int:pk>/delete/', views.supplier_delete, name='delete'),
]
