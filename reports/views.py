"""
Reports App - Views (PDF uses Rs. instead of rupee symbol to avoid font issues)
"""
import csv
import io
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Q, F


def _pdf_header(story, styles, title, subtitle=''):
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.units import mm
    story.append(Paragraph(title, styles['Title']))
    if subtitle:
        story.append(Paragraph(subtitle, styles['Normal']))
    story.append(Spacer(1, 5 * mm))


def _make_pdf_table(data, col_widths=None):
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return table


def _get_date_range(request, default_days=30):
    today = timezone.now().date()
    date_from = request.GET.get('date_from') or (today - timedelta(days=default_days)).isoformat()
    date_to = request.GET.get('date_to') or today.isoformat()
    return date_from, date_to


def _pdf_response(buffer, filename):
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _build_pdf(story, buffer, landscape_mode=True):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.units import mm
    pagesize = landscape(A4) if landscape_mode else A4
    doc = SimpleDocTemplate(buffer, pagesize=pagesize,
                            topMargin=15 * mm, bottomMargin=15 * mm,
                            leftMargin=15 * mm, rightMargin=15 * mm)
    doc.build(story)


@login_required
def report_home(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')
    return render(request, 'reports/home.html')


@login_required
def sales_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from sales.models import Sale
    date_from, date_to = _get_date_range(request)
    payment = request.GET.get('payment', '')

    sales = Sale.objects.filter(
        sale_date__date__gte=date_from,
        sale_date__date__lte=date_to,
        status='completed',
    ).select_related('customer', 'created_by').order_by('-sale_date')

    if payment:
        sales = sales.filter(payment_method=payment)

    totals = sales.aggregate(
        revenue=Sum('grand_total'),
        discount=Sum('discount_amount'),
        tax=Sum('gst_amount'),
        count=Count('id'),
    )

    return render(request, 'reports/sales.html', {
        'sales': sales,
        'date_from': date_from,
        'date_to': date_to,
        'selected_payment': payment,
        'payment_methods': Sale.PAYMENT_METHODS,
        'totals': totals,
    })


@login_required
def sales_report_pdf(request):
    if not request.user.is_manager:
        return HttpResponse('Unauthorized', status=401)

    from sales.models import Sale
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    date_from, date_to = _get_date_range(request)
    sales = Sale.objects.filter(
        sale_date__date__gte=date_from,
        sale_date__date__lte=date_to,
        status='completed',
    ).order_by('-sale_date')

    try:
        buffer = io.BytesIO()
        styles = getSampleStyleSheet()
        story = []
        _pdf_header(story, styles, 'Sales Report', f'Period: {date_from} to {date_to}')

        data = [['Invoice', 'Date', 'Customer', 'Subtotal', 'Discount', 'GST', 'Grand Total', 'Payment']]
        total = 0
        for s in sales:
            data.append([
                s.invoice_number,
                s.sale_date.strftime('%d/%m/%Y'),
                s.customer.name if s.customer else 'Walk-in',
                f'Rs.{s.subtotal}',
                f'Rs.{s.discount_amount}',
                f'Rs.{s.gst_amount}',
                f'Rs.{s.grand_total}',
                s.get_payment_method_display(),
            ])
            total += float(s.grand_total)
        data.append(['', '', 'TOTAL', '', '', '', f'Rs.{total:.2f}', ''])

        story.append(_make_pdf_table(data))
        _build_pdf(story, buffer, landscape_mode=True)
        return _pdf_response(buffer, f'sales_report_{date_from}_{date_to}.pdf')

    except ImportError:
        messages.error(request, 'ReportLab not installed.')
        return redirect('reports:sales')


@login_required
def sales_report_csv(request):
    if not request.user.is_manager:
        return HttpResponse('Unauthorized', status=401)

    from sales.models import Sale
    date_from, date_to = _get_date_range(request)
    sales = Sale.objects.filter(
        sale_date__date__gte=date_from,
        sale_date__date__lte=date_to,
    ).order_by('-sale_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_{date_from}_{date_to}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Invoice', 'Date', 'Customer', 'Subtotal', 'Discount', 'GST', 'Grand Total', 'Payment', 'Status'])
    for s in sales:
        writer.writerow([
            s.invoice_number,
            s.sale_date.strftime('%Y-%m-%d %H:%M'),
            s.customer.name if s.customer else 'Walk-in',
            s.subtotal, s.discount_amount, s.gst_amount, s.grand_total,
            s.get_payment_method_display(), s.get_status_display(),
        ])
    return response


@login_required
def purchase_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from purchase.models import PurchaseOrder
    date_from, date_to = _get_date_range(request)
    status = request.GET.get('status', '')

    orders = PurchaseOrder.objects.filter(
        order_date__gte=date_from,
        order_date__lte=date_to,
    ).select_related('supplier').order_by('-order_date')

    if status:
        orders = orders.filter(status=status)

    totals = orders.aggregate(
        total=Sum('total_amount'),
        paid=Sum('paid_amount'),
        count=Count('id'),
    )

    return render(request, 'reports/purchase.html', {
        'orders': orders,
        'date_from': date_from,
        'date_to': date_to,
        'selected_status': status,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
        'totals': totals,
    })


@login_required
def purchase_report_pdf(request):
    if not request.user.is_manager:
        return HttpResponse('Unauthorized', status=401)

    from purchase.models import PurchaseOrder
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    date_from, date_to = _get_date_range(request)
    orders = PurchaseOrder.objects.filter(
        order_date__gte=date_from,
        order_date__lte=date_to,
    ).select_related('supplier').order_by('-order_date')

    try:
        buffer = io.BytesIO()
        styles = getSampleStyleSheet()
        story = []
        _pdf_header(story, styles, 'Purchase Report', f'Period: {date_from} to {date_to}')

        data = [['PO Number', 'Date', 'Supplier', 'Status', 'Total', 'Paid', 'Balance']]
        for o in orders:
            data.append([
                o.order_number,
                str(o.order_date),
                o.supplier.company_name,
                o.get_status_display(),
                f'Rs.{o.total_amount}',
                f'Rs.{o.paid_amount}',
                f'Rs.{o.balance_amount}',
            ])

        story.append(_make_pdf_table(data))
        _build_pdf(story, buffer, landscape_mode=True)
        return _pdf_response(buffer, f'purchase_report_{date_from}_{date_to}.pdf')

    except ImportError:
        messages.error(request, 'ReportLab not installed.')
        return redirect('reports:purchase')


@login_required
def profit_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from sales.models import SaleItem
    date_from, date_to = _get_date_range(request)

    items = SaleItem.objects.filter(
        sale__sale_date__date__gte=date_from,
        sale__sale_date__date__lte=date_to,
        sale__status='completed',
    ).select_related('product', 'sale')

    rows = []
    total_revenue = 0
    total_cost = 0

    for item in items:
        revenue = float(item.total_price)
        cost = float(item.product.purchase_price) * item.quantity
        profit = revenue - cost
        total_revenue += revenue
        total_cost += cost
        rows.append({
            'invoice': item.sale.invoice_number,
            'date': item.sale.sale_date,
            'product': item.product.name,
            'qty': item.quantity,
            'revenue': revenue,
            'cost': cost,
            'profit': profit,
            'margin': round((profit / revenue * 100), 2) if revenue > 0 else 0,
        })

    total_profit = total_revenue - total_cost

    return render(request, 'reports/profit.html', {
        'rows': rows,
        'date_from': date_from,
        'date_to': date_to,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'profit_margin': round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0,
    })


@login_required
def inventory_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from products.models import Product, Category
    category_id = request.GET.get('category', '')
    stock_status = request.GET.get('stock_status', '')

    products = Product.objects.filter(is_active=True).select_related('category', 'brand', 'supplier')

    if category_id:
        products = products.filter(category_id=category_id)
    if stock_status == 'low':
        products = products.filter(stock_quantity__gt=0, stock_quantity__lte=F('low_stock_threshold'))
    elif stock_status == 'out':
        products = products.filter(stock_quantity__lte=0)
    elif stock_status == 'ok':
        products = products.filter(stock_quantity__gt=F('low_stock_threshold'))

    products = products.order_by('category__name', 'name')
    categories = Category.objects.filter(is_active=True)

    total_cost_value = sum(float(p.purchase_price) * p.stock_quantity for p in products)
    total_retail_value = sum(float(p.selling_price) * p.stock_quantity for p in products)

    return render(request, 'reports/inventory.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'selected_stock_status': stock_status,
        'total_cost_value': total_cost_value,
        'total_retail_value': total_retail_value,
    })


@login_required
def inventory_report_pdf(request):
    if not request.user.is_manager:
        return HttpResponse('Unauthorized', status=401)

    from products.models import Product
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    products = Product.objects.filter(is_active=True).select_related('category').order_by('category__name', 'name')

    try:
        buffer = io.BytesIO()
        styles = getSampleStyleSheet()
        story = []
        _pdf_header(story, styles, 'Inventory Report',
                    f'Generated: {timezone.now().strftime("%d %b %Y")}')

        data = [['Code', 'Product', 'Category', 'Stock', 'Cost Price', 'Selling Price', 'Stock Value']]
        for p in products:
            stock_value = float(p.purchase_price) * p.stock_quantity
            data.append([
                p.product_code,
                p.name[:35],
                p.category.name if p.category else '-',
                str(p.stock_quantity),
                f'Rs.{p.purchase_price}',
                f'Rs.{p.selling_price}',
                f'Rs.{stock_value:.2f}',
            ])

        story.append(_make_pdf_table(data))
        _build_pdf(story, buffer, landscape_mode=True)
        return _pdf_response(buffer, 'inventory_report.pdf')

    except ImportError:
        messages.error(request, 'ReportLab not installed.')
        return redirect('reports:inventory')


@login_required
def customer_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from customers.models import Customer
    customers = Customer.objects.annotate(
        total_spent=Sum('sales__grand_total'),
        order_count=Count('sales'),
    ).order_by('-total_spent')

    return render(request, 'reports/customers.html', {'customers': customers})


@login_required
def supplier_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from suppliers.models import Supplier
    suppliers = Supplier.objects.annotate(
        total_ordered=Sum('purchase_orders__total_amount'),
        total_paid=Sum('purchase_orders__paid_amount'),
        order_count=Count('purchase_orders'),
    ).order_by('-total_ordered')

    return render(request, 'reports/suppliers.html', {'suppliers': suppliers})


@login_required
def employee_report(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('dashboard:index')

    from employees.models import Employee
    employees = Employee.objects.filter(status='active').annotate(
        present_days=Count('attendances', filter=Q(attendances__status='present')),
        absent_days=Count('attendances', filter=Q(attendances__status='absent')),
    ).order_by('first_name')

    return render(request, 'reports/employees.html', {'employees': employees})
