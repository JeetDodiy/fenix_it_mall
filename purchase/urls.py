"""Purchase App – URLs"""
from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('', views.purchase_list, name='list'),
    path('add/', views.purchase_add, name='add'),
    path('<int:pk>/', views.purchase_detail, name='detail'),
    path('<int:pk>/edit/', views.purchase_edit, name='edit'),
    path('<int:pk>/receive/', views.receive_stock, name='receive_stock'),
    path('<int:pk>/payment/', views.add_payment, name='add_payment'),
    path('<int:pk>/invoice/', views.purchase_invoice, name='invoice'),
    path('<int:pk>/delete/', views.purchase_delete, name='delete'),
]
