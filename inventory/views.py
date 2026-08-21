"""
Inventory App – Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum
from products.models import Product, Category
from .models import StockMovement, StockAdjustment
from .forms import StockAdjustmentForm
from notifications.utils import create_stock_notification


@login_required
def stock_list(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    stock_status = request.GET.get('stock_status', '')

    products = Product.objects.filter(is_active=True).select_related('category', 'brand')

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(product_code__icontains=q)
        )
    if category:
        products = products.filter(category_id=category)
    if stock_status == 'low':
        products = products.filter(stock_quantity__gt=0, stock_quantity__lte=F('low_stock_threshold'))
    elif stock_status == 'out':
        products = products.filter(stock_quantity__lte=0)
    elif stock_status == 'ok':
        products = products.filter(stock_quantity__gt=F('low_stock_threshold'))

    products = products.order_by('name')
    paginator = Paginator(products, 20)
    page = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.filter(is_active=True)
    all_products = Product.objects.filter(is_active=True)
    total_stock_value = all_products.aggregate(
        val=Sum(F('stock_quantity') * F('purchase_price'))
    )['val'] or 0
    total_retail_value = all_products.aggregate(
        val=Sum(F('stock_quantity') * F('selling_price'))
    )['val'] or 0

    return render(request, 'inventory/list.html', {
        'products': page,
        'categories': categories,
        'q': q,
        'selected_category': category,
        'selected_stock_status': stock_status,
        'total_stock_value': total_stock_value,
        'total_retail_value': total_retail_value,
    })


@login_required
def low_stock(request):
    products = Product.objects.filter(
        is_active=True,
        stock_quantity__lte=F('low_stock_threshold')
    ).select_related('category').order_by('stock_quantity')
    return render(request, 'inventory/low_stock.html', {'products': products})


@login_required
def out_of_stock(request):
    products = Product.objects.filter(
        is_active=True,
        stock_quantity__lte=0
    ).select_related('category').order_by('name')
    return render(request, 'inventory/out_of_stock.html', {'products': products})


@login_required
def stock_in(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('inventory:list')

    form = StockAdjustmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        adj = form.save(commit=False)
        adj.adjustment_type = 'add'
        adj.created_by = request.user
        adj.save()
        messages.success(request, f'Stock added for {adj.product.name}: +{adj.quantity}')
        return redirect('inventory:list')

    # Force add type
    form.fields['adjustment_type'].initial = 'add'
    return render(request, 'inventory/stock_in.html', {'form': form, 'title': 'Stock In'})


@login_required
def stock_out(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('inventory:list')

    form = StockAdjustmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        adj = form.save(commit=False)
        adj.adjustment_type = 'reduce'
        adj.created_by = request.user
        product = adj.product
        if product.stock_quantity < adj.quantity:
            messages.error(request, f'Insufficient stock. Only {product.stock_quantity} available.')
        else:
            adj.save()
            # Fire notification if stock drops low or hits zero
            adj.product.refresh_from_db()
            create_stock_notification(adj.product, triggered_by_user=request.user)
            messages.success(request, f'Stock removed for {adj.product.name}: -{adj.quantity}')
            return redirect('inventory:list')

    form.fields['adjustment_type'].initial = 'reduce'
    return render(request, 'inventory/stock_out.html', {'form': form, 'title': 'Stock Out'})


@login_required
def stock_adjust(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('inventory:list')

    product_id = request.GET.get('product')
    initial = {}
    if product_id:
        initial['product'] = product_id

    form = StockAdjustmentForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        adj = form.save(commit=False)
        adj.created_by = request.user
        if adj.adjustment_type == 'reduce' and adj.product.stock_quantity < adj.quantity:
            messages.error(request, f'Insufficient stock. Only {adj.product.stock_quantity} available.')
        else:
            adj.save()
            # Fire notification if stock drops low or hits zero after a reduce
            if adj.adjustment_type == 'reduce':
                adj.product.refresh_from_db()
                create_stock_notification(adj.product, triggered_by_user=request.user)
            messages.success(request, f'Stock adjusted for {adj.product.name}.')
            return redirect('inventory:history')

    return render(request, 'inventory/adjust.html', {'form': form})


@login_required
def stock_history(request):
    q = request.GET.get('q', '')
    movement_type = request.GET.get('type', '')

    movements = StockMovement.objects.select_related('product', 'created_by').order_by('-created_at')
    if q:
        movements = movements.filter(product__name__icontains=q)
    if movement_type:
        movements = movements.filter(movement_type=movement_type)

    paginator = Paginator(movements, 30)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'inventory/history.html', {
        'movements': page,
        'q': q,
        'selected_type': movement_type,
        'movement_types': StockMovement.MOVEMENT_TYPES,
    })


@login_required
def damaged_stock(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('inventory:list')

    form = StockAdjustmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        adj = form.save(commit=False)
        adj.adjustment_type = 'reduce'
        adj.created_by = request.user
        product = adj.product
        if product.stock_quantity < adj.quantity:
            messages.error(request, f'Insufficient stock. Only {product.stock_quantity} available.')
        else:
            adj.save()
            # Override movement type to 'damaged'
            StockMovement.objects.filter(
                product=adj.product,
                reference=f'Adjustment #{adj.pk}'
            ).update(movement_type='damaged')
            # Fire notification – damaged stock may push item to low/zero
            adj.product.refresh_from_db()
            create_stock_notification(adj.product, triggered_by_user=request.user)
            messages.success(request, f'Damaged stock recorded for {adj.product.name}.')
            return redirect('inventory:list')

    return render(request, 'inventory/damaged.html', {'form': form, 'title': 'Record Damaged Stock'})
