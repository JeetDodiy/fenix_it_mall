"""
Dashboard App – Views with aggregated stats and chart data
"""
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, date


@login_required
def index(request):
    from products.models import Product, Category, Brand
    from customers.models import Customer
    from suppliers.models import Supplier
    from sales.models import Sale, SaleItem
    from purchase.models import PurchaseOrder
    from employees.models import Employee
    from inventory.models import StockMovement
    from notifications.models import Notification

    # Use localdate() so date comparisons are correct in IST (Asia/Kolkata)
    today     = timezone.localdate()
    yesterday = today - timedelta(days=1)
    month_start = today.replace(day=1)

    # ─── Stat Cards ───
    total_products  = Product.objects.filter(is_active=True).count()
    total_categories= Category.objects.filter(is_active=True).count()
    total_brands    = Brand.objects.filter(is_active=True).count()
    total_customers = Customer.objects.filter(is_active=True).count()
    total_suppliers = Supplier.objects.filter(is_active=True).count()
    total_employees = Employee.objects.filter(status='active').count()
    pending_po_count= PurchaseOrder.objects.filter(status='pending').count()

    # ─── Sales Today / Yesterday ───
    today_sales_qs     = Sale.objects.filter(sale_date__date=today,     status='completed')
    yesterday_sales_qs = Sale.objects.filter(sale_date__date=yesterday, status='completed')

    today_sales_count     = today_sales_qs.count()
    today_revenue         = today_sales_qs.aggregate(t=Sum('grand_total'))['t'] or 0
    yesterday_revenue     = yesterday_sales_qs.aggregate(t=Sum('grand_total'))['t'] or 0
    yesterday_sales_count = yesterday_sales_qs.count()

    # Revenue trend % vs yesterday
    if yesterday_revenue and yesterday_revenue > 0:
        revenue_trend = round(((float(today_revenue) - float(yesterday_revenue)) / float(yesterday_revenue)) * 100, 1)
    elif today_revenue > 0:
        revenue_trend = 100.0
    else:
        revenue_trend = None

    # Count trend % vs yesterday
    if yesterday_sales_count > 0:
        count_trend = round(((today_sales_count - yesterday_sales_count) / yesterday_sales_count) * 100, 1)
    elif today_sales_count > 0:
        count_trend = 100.0
    else:
        count_trend = None

    # ─── Today's Profit ───
    today_items = SaleItem.objects.filter(
        sale__sale_date__date=today, sale__status='completed'
    ).select_related('product')
    today_profit = sum(
        (item.unit_price - item.product.purchase_price) * item.quantity
        for item in today_items
    )

    # ─── Monthly Sales ───
    monthly_sales_qs = Sale.objects.filter(
        sale_date__date__gte=month_start, status='completed'
    )
    monthly_revenue    = monthly_sales_qs.aggregate(t=Sum('grand_total'))['t'] or 0
    monthly_sales_count= monthly_sales_qs.count()

    # Monthly profit
    total_sale_items = SaleItem.objects.filter(
        sale__sale_date__date__gte=month_start, sale__status='completed'
    ).select_related('product')
    monthly_profit = sum(
        (item.unit_price - item.product.purchase_price) * item.quantity
        for item in total_sale_items
    )

    # ─── Stock Status ───
    low_stock_count   = Product.objects.filter(is_active=True, stock_quantity__gt=0, stock_quantity__lte=5).count()
    out_of_stock_count= Product.objects.filter(is_active=True, stock_quantity__lte=0).count()
    in_stock_count    = Product.objects.filter(is_active=True, stock_quantity__gt=5).count()

    # Low-stock items for the alerts panel (key must match template: low_stock_items)
    low_stock_items = Product.objects.filter(
        is_active=True, stock_quantity__lte=5
    ).order_by('stock_quantity').prefetch_related('images')[:5]

    # ─── Monthly Chart Data (last 6 months) ───
    chart_labels  = []
    chart_sales   = []
    chart_revenue = []
    chart_profit  = []

    for i in range(5, -1, -1):
        d = today - timedelta(days=30 * i)
        month_label = d.strftime('%b %Y')
        m_start = d.replace(day=1)
        if d.month == 12:
            m_end = d.replace(year=d.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            m_end = d.replace(month=d.month + 1, day=1) - timedelta(days=1)

        m_sales = Sale.objects.filter(
            sale_date__date__gte=m_start,
            sale_date__date__lte=m_end,
            status='completed'
        )
        m_revenue = m_sales.aggregate(t=Sum('grand_total'))['t'] or 0
        m_items = SaleItem.objects.filter(
            sale__sale_date__date__gte=m_start,
            sale__sale_date__date__lte=m_end,
            sale__status='completed'
        ).select_related('product')
        m_profit = sum(
            (item.unit_price - item.product.purchase_price) * item.quantity
            for item in m_items
        )

        chart_labels.append(month_label)
        chart_sales.append(m_sales.count())
        chart_revenue.append(float(m_revenue))
        chart_profit.append(float(m_profit))

    # ─── Category Distribution ───
    categories = Category.objects.annotate(pcount=Count('products')).filter(pcount__gt=0)[:8]
    category_labels = [c.name for c in categories]
    category_values = [c.pcount for c in categories]

    # ─── Best Selling Products (last 30 days) ───
    thirty_days_ago = today - timedelta(days=30)
    best_sellers = SaleItem.objects.filter(
        sale__sale_date__date__gte=thirty_days_ago,
        sale__status='completed'
    ).values('product__name').annotate(
        total_qty=Sum('quantity')
    ).order_by('-total_qty')[:5]

    best_seller_labels = [b['product__name'][:20] for b in best_sellers]
    best_seller_values = [b['total_qty'] for b in best_sellers]

    # ─── Recent Sales ───
    recent_sales = Sale.objects.select_related('customer', 'created_by').order_by('-sale_date')[:8]

    # ─── Recent Notifications ───
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]

    # ─── Recent Stock Movements ───
    recent_movements = StockMovement.objects.select_related('product', 'created_by').order_by('-created_at')[:6]

    context = {
        # Counts
        'total_products':    total_products,
        'total_categories':  total_categories,
        'total_brands':      total_brands,
        'total_customers':   total_customers,
        'total_suppliers':   total_suppliers,
        'total_employees':   total_employees,
        'pending_po_count':  pending_po_count,

        # Today's KPIs
        'today_sales_count':     today_sales_count,
        'today_revenue':         today_revenue,
        'today_profit':          today_profit,
        'yesterday_sales_count': yesterday_sales_count,
        'revenue_trend':         revenue_trend,
        'count_trend':           count_trend,

        # Monthly
        'monthly_revenue':     monthly_revenue,
        'monthly_sales_count': monthly_sales_count,
        'monthly_profit':      monthly_profit,

        # Stock
        'low_stock_count':    low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'in_stock_count':     in_stock_count,
        'low_stock_items':    low_stock_items,   # ← fixed: was top_low_stock

        # Charts
        'chart_labels':         json.dumps(chart_labels),
        'chart_sales':          json.dumps(chart_sales),
        'chart_revenue':        json.dumps(chart_revenue),
        'chart_profit':         json.dumps(chart_profit),
        'category_labels':      json.dumps(category_labels),
        'category_values':      json.dumps(category_values),
        'inventory_status':     json.dumps([in_stock_count, low_stock_count, out_of_stock_count]),
        'best_seller_labels':   json.dumps(best_seller_labels),
        'best_seller_values':   json.dumps(best_seller_values),

        # Recent data
        'recent_sales':      recent_sales,
        'notifications':     notifications,
        'recent_movements':  recent_movements,
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def chart_data(request):
    """AJAX endpoint – returns latest chart data as JSON for live refresh"""
    from sales.models import Sale, SaleItem

    today = timezone.localdate()
    chart_labels  = []
    chart_revenue = []
    chart_profit  = []
    chart_sales   = []

    from datetime import timedelta
    for i in range(5, -1, -1):
        d = today - timedelta(days=30 * i)
        m_start = d.replace(day=1)
        if d.month == 12:
            m_end = d.replace(year=d.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            m_end = d.replace(month=d.month + 1, day=1) - timedelta(days=1)

        m_sales   = Sale.objects.filter(sale_date__date__gte=m_start, sale_date__date__lte=m_end, status='completed')
        m_revenue = m_sales.aggregate(t=Sum('grand_total'))['t'] or 0
        m_items   = SaleItem.objects.filter(
            sale__sale_date__date__gte=m_start,
            sale__sale_date__date__lte=m_end,
            sale__status='completed'
        ).select_related('product')
        m_profit = sum((item.unit_price - item.product.purchase_price) * item.quantity for item in m_items)

        chart_labels.append(d.strftime('%b %Y'))
        chart_revenue.append(float(m_revenue))
        chart_profit.append(float(m_profit))
        chart_sales.append(m_sales.count())

    return JsonResponse({
        'labels':  chart_labels,
        'revenue': chart_revenue,
        'profit':  chart_profit,
        'sales':   chart_sales,
    })


@login_required
def recent_activity(request):
    from inventory.models import StockMovement
    from sales.models import Sale, SaleItem
    movements    = StockMovement.objects.select_related('product').order_by('-created_at')[:10]
    recent_sales = Sale.objects.select_related('customer').order_by('-sale_date')[:5]
    frequent_items = SaleItem.objects.values('product__name').annotate(count=Count('product')).order_by('-count')[:5]
    return render(request, 'dashboard/recent_activity.html', {
        'movements':      movements,
        'recent_sales':   recent_sales,
        'frequent_items': frequent_items,
    })
