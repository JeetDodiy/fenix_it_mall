"""Employees App – URLs"""
from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='list'),
    path('add/', views.employee_add, name='add'),
    path('<int:pk>/', views.employee_detail, name='detail'),
    path('<int:pk>/edit/', views.employee_edit, name='edit'),
    path('<int:pk>/delete/', views.employee_delete, name='delete'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/save/', views.attendance_add, name='attendance_add'),
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/apply/', views.leave_add, name='leave_add'),
    path('leaves/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
]
