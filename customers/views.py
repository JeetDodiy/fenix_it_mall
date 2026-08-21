"""
Customers App – Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    q = request.GET.get('q', '')
    customers = Customer.objects.all().order_by('-created_at')

    if q:
        customers = customers.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q)
        )

    paginator = Paginator(customers, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'customers/list.html', {'customers': page, 'q': q})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    from sales.models import Sale
    sales = Sale.objects.filter(customer=customer).order_by('-created_at')
    total_spent = sales.filter(status='completed').aggregate(t=Sum('grand_total'))['t'] or 0
    total_orders = sales.count()

    paginator = Paginator(sales, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'customers/detail.html', {
        'customer': customer,
        'sales': page,
        'total_spent': total_spent,
        'total_orders': total_orders,
    })


@login_required
def customer_add(request):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully.')
        return redirect('customers:list')
    return render(request, 'customers/form.html', {'form': form, 'title': 'Add Customer'})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer updated.')
        return redirect('customers:detail', pk=customer.pk)
    return render(request, 'customers/form.html', {
        'form': form,
        'title': f'Edit – {customer.name}',
        'customer': customer,
    })


@login_required
def customer_delete(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('customers:list')

    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted.')
        return redirect('customers:list')
    return render(request, 'customers/delete_confirm.html', {'customer': customer})
