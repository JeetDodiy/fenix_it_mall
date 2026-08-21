"""Sales App – URLs"""
from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.sale_list, name='list'),
    path('pos/', views.pos, name='pos'),
    path('create/', views.sale_create, name='create'),
    path('<int:pk>/', views.sale_detail, name='detail'),
    path('<int:pk>/invoice/', views.sale_invoice, name='invoice'),
    path('<int:pk>/invoice/pdf/', views.sale_invoice_pdf, name='invoice_pdf'),
    path('<int:pk>/edit/', views.sale_edit, name='edit'),
    path('<int:pk>/void/', views.sale_void, name='void'),
    path('<int:pk>/log-print/', views.sale_log_print, name='log_print'),
    path('<int:pk>/delete/', views.sale_delete, name='delete'),
]
