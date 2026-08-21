"""Inventory App – URLs"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.stock_list, name='list'),
    path('low-stock/', views.low_stock, name='low_stock'),
    path('out-of-stock/', views.out_of_stock, name='out_of_stock'),
    path('stock-in/', views.stock_in, name='stock_in'),
    path('stock-out/', views.stock_out, name='stock_out'),
    path('adjust/', views.stock_adjust, name='adjust'),
    path('history/', views.stock_history, name='history'),
    path('damaged/', views.damaged_stock, name='damaged'),
]
