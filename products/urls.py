from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Products
    path('', views.product_list, name='list'),
    path('add/', views.product_add, name='add'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('<int:pk>/edit/', views.product_edit, name='edit'),
    path('<int:pk>/delete/', views.product_delete, name='delete'),
    path('<int:pk>/barcode/', views.product_barcode, name='barcode'),
    path('<int:pk>/qrcode/', views.product_qrcode, name='qrcode'),
    path('<int:pk>/regenerate-codes/', views.regenerate_barcode_qr, name='regenerate_codes'),
    path('search/', views.product_search_ajax, name='search_ajax'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Brands
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/add/', views.brand_add, name='brand_add'),
    path('brands/<int:pk>/edit/', views.brand_edit, name='brand_edit'),
    path('brands/<int:pk>/delete/', views.brand_delete, name='brand_delete'),
]
