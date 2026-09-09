"""Reports App – URLs"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_home, name='home'),
    path('sales/', views.sales_report, name='sales'),
    path('sales/pdf/', views.sales_report_pdf, name='sales_pdf'),
    path('sales/csv/', views.sales_report_csv, name='sales_csv'),
    path('purchase/', views.purchase_report, name='purchase'),
    path('purchase/pdf/', views.purchase_report_pdf, name='purchase_pdf'),
    path('profit/', views.profit_report, name='profit'),
    path('inventory/', views.inventory_report, name='inventory'),
    path('inventory/pdf/', views.inventory_report_pdf, name='inventory_pdf'),
    path('customers/', views.customer_report, name='customers'),
    path('suppliers/', views.supplier_report, name='suppliers'),
    path('suppliers/pdf/', views.supplier_report_pdf, name='suppliers_pdf'),
    path('suppliers/csv/', views.supplier_report_csv, name='suppliers_csv'),
    path('employees/', views.employee_report, name='employees'),
]
