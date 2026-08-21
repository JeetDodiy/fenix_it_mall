"""
Employees App – Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Employee, Attendance, Leave
from .forms import EmployeeForm, AttendanceForm, LeaveForm


@login_required
def employee_list(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    employees = Employee.objects.all().order_by('first_name')

    if q:
        employees = employees.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(employee_id__icontains=q) | Q(designation__icontains=q)
        )
    if status:
        employees = employees.filter(status=status)

    paginator = Paginator(employees, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'employees/list.html', {
        'employees': page,
        'q': q,
        'selected_status': status,
        'status_choices': Employee.STATUS_CHOICES,
    })


@login_required
def employee_detail(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    employee = get_object_or_404(Employee, pk=pk)
    recent_attendance = Attendance.objects.filter(employee=employee).order_by('-date')[:10]
    recent_leaves = Leave.objects.filter(employee=employee).order_by('-created_at')[:5]

    return render(request, 'employees/detail.html', {
        'employee': employee,
        'recent_attendance': recent_attendance,
        'recent_leaves': recent_leaves,
    })


@login_required
def employee_add(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    form = EmployeeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Employee added successfully.')
        return redirect('employees:list')
    return render(request, 'employees/form.html', {'form': form, 'title': 'Add Employee'})


@login_required
def employee_edit(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, request.FILES or None, instance=employee)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Employee updated.')
        return redirect('employees:detail', pk=employee.pk)
    return render(request, 'employees/form.html', {
        'form': form,
        'title': f'Edit – {employee.full_name}',
        'employee': employee,
    })


@login_required
def employee_delete(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('employees:list')

    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.status = 'terminated'
        employee.save()
        messages.success(request, f'{employee.full_name} marked as terminated.')
        return redirect('employees:list')
    return render(request, 'employees/delete_confirm.html', {'employee': employee})


@login_required
def attendance_list(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    date_str = request.GET.get('date', timezone.now().date().isoformat())
    employees = Employee.objects.filter(status='active').order_by('first_name')

    attendance_map = {
        a.employee_id: a
        for a in Attendance.objects.filter(date=date_str)
    }
    attendance_data = [
        {'employee': emp, 'attendance': attendance_map.get(emp.pk)}
        for emp in employees
    ]

    return render(request, 'employees/attendance.html', {
        'attendance_data': attendance_data,
        'date_str': date_str,
    })


@login_required
def attendance_add(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    if request.method == 'POST':
        date_str = request.POST.get('date', timezone.now().date().isoformat())
        employees = Employee.objects.filter(status='active')

        for emp in employees:
            status_val = request.POST.get(f'status_{emp.pk}', 'absent')
            check_in = request.POST.get(f'check_in_{emp.pk}') or None
            check_out = request.POST.get(f'check_out_{emp.pk}') or None

            att, created = Attendance.objects.update_or_create(
                employee=emp,
                date=date_str,
                defaults={'status': status_val, 'check_in': check_in, 'check_out': check_out},
            )

        messages.success(request, f'Attendance saved for {date_str}.')
        return redirect(f"{request.path}?date={date_str}".replace('add', 'list') + f'?date={date_str}')

    return redirect('employees:attendance_list')


@login_required
def leave_list(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    status = request.GET.get('status', '')
    leaves = Leave.objects.select_related('employee', 'approved_by').order_by('-created_at')
    if status:
        leaves = leaves.filter(status=status)

    paginator = Paginator(leaves, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'employees/leaves.html', {
        'leaves': page,
        'selected_status': status,
        'status_choices': Leave.STATUS_CHOICES,
    })


@login_required
def leave_add(request):
    form = LeaveForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Leave request submitted.')
        return redirect('employees:leave_list')
    return render(request, 'employees/leave_form.html', {'form': form, 'title': 'Apply for Leave'})


@login_required
def leave_approve(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('employees:leave_list')

    leave = get_object_or_404(Leave, pk=pk)
    action = request.POST.get('action')
    if action == 'approve':
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.save()
        messages.success(request, 'Leave approved.')
    elif action == 'reject':
        leave.status = 'rejected'
        leave.approved_by = request.user
        leave.save()
        messages.success(request, 'Leave rejected.')
    return redirect('employees:leave_list')
