from django.contrib import admin
from .models import Employee, Attendance, Leave


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'designation', 'department', 'salary', 'status', 'join_date')
    list_filter = ('status', 'department')
    search_fields = ('first_name', 'last_name', 'employee_id', 'designation')
    readonly_fields = ('employee_id', 'created_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in', 'check_out')
    list_filter = ('status', 'date')
    search_fields = ('employee__first_name', 'employee__last_name')
    date_hierarchy = 'date'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__first_name', 'employee__last_name')
