"""
Suppliers App – Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Supplier
from .forms import SupplierForm


@login_required
def supplier_list(request):
    q = request.GET.get('q', '')
    suppliers = Supplier.objects.all().order_by('company_name')

    if q:
        suppliers = suppliers.filter(
            Q(company_name__icontains=q) | Q(contact_person__icontains=q) | Q(phone__icontains=q)
        )

    paginator = Paginator(suppliers, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'suppliers/list.html', {'suppliers': page, 'q': q})


@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    from purchase.models import PurchaseOrder
    orders = PurchaseOrder.objects.filter(supplier=supplier).order_by('-created_at')
    total_ordered = orders.aggregate(t=Sum('total_amount'))['t'] or 0
    total_paid = orders.aggregate(t=Sum('paid_amount'))['t'] or 0
    total_orders = orders.count()

    paginator = Paginator(orders, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'suppliers/detail.html', {
        'supplier': supplier,
        'orders': page,
        'total_ordered': total_ordered,
        'total_paid': total_paid,
        'outstanding': total_ordered - total_paid,
        'total_orders': total_orders,
    })


@login_required
def supplier_add(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('suppliers:list')

    form = SupplierForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Supplier added successfully.')
        return redirect('suppliers:list')
    return render(request, 'suppliers/form.html', {'form': form, 'title': 'Add Supplier'})


@login_required
def supplier_edit(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('suppliers:list')

    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated.')
        return redirect('suppliers:detail', pk=supplier.pk)
    return render(request, 'suppliers/form.html', {
        'form': form,
        'title': f'Edit – {supplier.company_name}',
        'supplier': supplier,
    })


@login_required
def supplier_delete(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('suppliers:list')

    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted.')
        return redirect('suppliers:list')
    return render(request, 'suppliers/delete_confirm.html', {'supplier': supplier})
