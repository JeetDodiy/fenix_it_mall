"""
Purchase App – Views (Decimal-safe)
"""
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from .models import PurchaseOrder, PurchaseItem, SupplierPayment
from .forms import PurchaseOrderForm, PurchaseOrderItemFormSet, SupplierPaymentForm


@login_required
def purchase_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    orders = PurchaseOrder.objects.select_related('supplier').order_by('-created_at')
    if q:
        orders = orders.filter(
            Q(order_number__icontains=q) | Q(supplier__company_name__icontains=q)
        )
    if status:
        orders = orders.filter(status=status)
    paginator = Paginator(orders, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'purchase/list.html', {
        'orders': page, 'q': q,
        'selected_status': status,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
    })


@login_required
def purchase_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    payments = order.payments.all()
    return render(request, 'purchase/detail.html', {'order': order, 'payments': payments})


@login_required
def purchase_add(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('purchase:list')

    form = PurchaseOrderForm(request.POST or None)
    formset = PurchaseOrderItemFormSet(request.POST or None)

    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        try:
            with transaction.atomic():
                order = form.save(commit=False)
                order.created_by = request.user
                order.save()
                formset.instance = order
                items = formset.save(commit=False)
                total = Decimal('0')
                for item in items:
                    item.purchase_order = order
                    item.save()
                    total += Decimal(str(item.quantity)) * item.purchase_price
                for obj in formset.deleted_objects:
                    obj.delete()
                order.total_amount = total
                order.save()
                messages.success(request, f'Purchase Order {order.order_number} created.')
                return redirect('purchase:detail', pk=order.pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'purchase/form.html', {
        'form': form, 'formset': formset, 'title': 'Create Purchase Order',
    })


@login_required
def purchase_edit(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('purchase:list')

    order = get_object_or_404(PurchaseOrder, pk=pk)
    
    # Allow editing of all orders except cancelled
    if order.status == 'cancelled':
        messages.error(request, 'Cannot edit a cancelled order.')
        return redirect('purchase:detail', pk=pk)

    form = PurchaseOrderForm(request.POST or None, instance=order)
    formset = PurchaseOrderItemFormSet(request.POST or None, instance=order)

    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        try:
            with transaction.atomic():
                order = form.save()
                items = formset.save(commit=False)
                total = Decimal('0')
                for item in items:
                    item.save()
                    total += Decimal(str(item.quantity)) * item.purchase_price
                for obj in formset.deleted_objects:
                    obj.delete()
                order.total_amount = total
                order.save()
                messages.success(request, f'Purchase Order {order.order_number} updated.')
                return redirect('purchase:detail', pk=order.pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'purchase/form.html', {
        'form': form, 'formset': formset,
        'title': f'Edit PO – {order.order_number}', 'order': order,
    })


@login_required
def receive_stock(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('purchase:list')

    order = get_object_or_404(PurchaseOrder, pk=pk)
    if order.status == 'received':
        messages.warning(request, 'This order is already fully received.')
        return redirect('purchase:detail', pk=pk)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                from inventory.models import StockMovement
                
                total_received = 0
                total_ordered = 0
                
                for item in order.items.select_related('product').all():
                    # Get quantity to receive from POST data
                    receive_qty_key = f'receive_qty_{item.pk}'
                    receive_qty = int(request.POST.get(receive_qty_key, 0))
                    
                    if receive_qty > 0:
                        # Update stock
                        qty_before = item.product.stock_quantity
                        item.product.stock_quantity += receive_qty
                        item.product.purchase_price = item.purchase_price
                        item.product.save()
                        
                        # Update received quantity
                        item.received_quantity += receive_qty
                        item.save()
                        
                        # Create stock movement
                        StockMovement.objects.create(
                            product=item.product,
                            movement_type='in',
                            quantity=receive_qty,
                            quantity_before=qty_before,
                            quantity_after=item.product.stock_quantity,
                            reference=f'PO: {order.order_number}',
                            created_by=request.user,
                        )
                    
                    total_received += item.received_quantity
                    total_ordered += item.quantity
                
                # Update order status
                if total_received >= total_ordered:
                    order.status = 'received'
                elif total_received > 0:
                    order.status = 'partial'
                
                order.save()
                messages.success(request, f'Stock received for PO {order.order_number}.')
                return redirect('purchase:detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')

    return render(request, 'purchase/receive_confirm.html', {'order': order})


@login_required
def add_payment(request, pk):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('purchase:list')

    order = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'POST':
        try:
            amount = Decimal(str(request.POST.get('amount', '0')))
        except Exception:
            messages.error(request, 'Invalid amount.')
            return render(request, 'purchase/payment_form.html', {'order': order})

        method = request.POST.get('payment_method', 'cash')
        note = request.POST.get('note', '')

        if amount <= 0:
            messages.error(request, 'Amount must be greater than 0.')
        elif amount > order.balance_amount:
            messages.error(request, f'Amount exceeds outstanding balance of Rs.{order.balance_amount}.')
        else:
            SupplierPayment.objects.create(
                purchase_order=order,
                amount=amount,
                payment_method=method,
                note=note,
                created_by=request.user,
            )
            order.paid_amount += amount
            order.save()
            messages.success(request, f'Payment of Rs.{amount} recorded successfully.')
            return redirect('purchase:detail', pk=pk)

    return render(request, 'purchase/payment_form.html', {'order': order})


@login_required
def purchase_invoice(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    from settings_app.models import CompanySettings
    company = CompanySettings.get_settings()
    return render(request, 'purchase/invoice.html', {'order': order, 'company': company})


@login_required
def purchase_delete(request, pk):
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('purchase:list')

    order = get_object_or_404(PurchaseOrder, pk=pk)
    if order.status == 'received':
        messages.error(request, 'Cannot delete a received order.')
        return redirect('purchase:detail', pk=pk)

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Purchase order deleted.')
        return redirect('purchase:list')

    return render(request, 'purchase/delete_confirm.html', {'order': order})
