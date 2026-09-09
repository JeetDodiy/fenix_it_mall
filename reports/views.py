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

    from decimal import Decimal
    from suppliers.models import Supplier
    from purchase.models import PurchaseOrder

    supplier_id = request.GET.get('supplier', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    payment_status = request.GET.get('payment_status', '')
    q = request.GET.get('q', '').strip()

    orders = PurchaseOrder.objects.all().select_related('supplier', 'created_by').prefetch_related('items__product', 'payments__created_by').order_by('-order_date', '-id')

    selected_supplier = None
    if supplier_id:
        try:
            selected_supplier = Supplier.objects.get(pk=supplier_id)
            orders = orders.filter(supplier=selected_supplier)
        except (Supplier.DoesNotExist, ValueError):
            supplier_id = ''

    if date_from:
        orders = orders.filter(order_date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__lte=date_to)

    if q:
        orders = orders.filter(
            Q(bill_number__icontains=q) |
            Q(order_number__icontains=q) |
            Q(supplier__company_name__icontains=q) |
            Q(supplier__contact_person__icontains=q) |
            Q(notes__icontains=q)
        )

    if payment_status == 'paid':
        orders = orders.filter(paid_amount__gte=F('total_amount'))
    elif payment_status == 'partial':
        orders = orders.filter(paid_amount__gt=0, paid_amount__lt=F('total_amount'))
    elif payment_status == 'unpaid':
        orders = orders.filter(paid_amount=0)

    # Calculate overall summary metrics
    totals = orders.aggregate(
        total_billed=Sum('total_amount'),
        total_given=Sum('paid_amount'),
        bill_count=Count('id'),
    )
    total_billed = totals['total_billed'] or Decimal('0')
    total_given = totals['total_given'] or Decimal('0')
    total_pending = total_billed - total_given
    bill_count = totals['bill_count'] or 0

    all_suppliers = Supplier.objects.all().order_by('company_name')

    # Supplier ledger breakdown
    supplier_ledgers = []
    for s in all_suppliers:
        s_orders = s.purchase_orders.all()
        if date_from:
            s_orders = s_orders.filter(order_date__gte=date_from)
        if date_to:
            s_orders = s_orders.filter(order_date__lte=date_to)
        agg = s_orders.aggregate(
            billed=Sum('total_amount'),
            paid=Sum('paid_amount'),
            count=Count('id'),
        )
        s_billed = agg['billed'] or Decimal('0')
        s_paid = agg['paid'] or Decimal('0')
        s_pending = s_billed - s_paid
        supplier_ledgers.append({
            'supplier': s,
            'bill_count': agg['count'] or 0,
            'total_billed': s_billed,
            'total_paid': s_paid,
            'pending_balance': s_pending,
            'status': 'Settled' if s_pending <= 0 else 'Pending Due',
        })

    return render(request, 'reports/suppliers.html', {
        'orders': orders,
        'suppliers': all_suppliers,
        'selected_supplier': selected_supplier,
        'selected_supplier_id': int(supplier_id) if supplier_id and supplier_id.isdigit() else '',
        'date_from': date_from,
        'date_to': date_to,
        'payment_status': payment_status,
        'q': q,
        'total_billed': total_billed,
        'total_given': total_given,
        'total_pending': total_pending,
        'bill_count': bill_count,
        'supplier_ledgers': supplier_ledgers,
    })


@login_required
def supplier_report_pdf(request):
    if not request.user.is_manager:
        return HttpResponse('Unauthorized', status=401)

    from decimal import Decimal
    from suppliers.models import Supplier
    from purchase.models import PurchaseOrder
    from reportlab.lib.styles import getSampleStyleSheet

    supplier_id = request.GET.get('supplier', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    payment_status = request.GET.get('payment_status', '')
    q = request.GET.get('q', '').strip()

    orders = PurchaseOrder.objects.all().select_related('supplier').prefetch_related('items__product').order_by('-order_date', '-id')

    selected_supplier_name = "All Suppliers"
    if supplier_id:
        try:
            supplier_obj = Supplier.objects.get(pk=supplier_id)
            orders = orders.filter(supplier=supplier_obj)
            selected_supplier_name = supplier_obj.company_name
        except (Supplier.DoesNotExist, ValueError):
            pass

    if date_from:
        orders = orders.filter(order_date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__lte=date_to)

    if q:
        orders = orders.filter(
            Q(bill_number__icontains=q) |
            Q(order_number__icontains=q) |
            Q(supplier__company_name__icontains=q) |
            Q(notes__icontains=q)
        )

    if payment_status == 'paid':
        orders = orders.filter(paid_amount__gte=F('total_amount'))
    elif payment_status == 'partial':
        orders = orders.filter(paid_amount__gt=0, paid_amount__lt=F('total_amount'))
    elif payment_status == 'unpaid':
        orders = orders.filter(paid_amount=0)

    totals = orders.aggregate(
        total_billed=Sum('total_amount'),
        total_given=Sum('paid_amount'),
        bill_count=Count('id'),
    )
    total_billed = totals['total_billed'] or Decimal('0')
    total_given = totals['total_given'] or Decimal('0')
    total_pending = total_billed - total_given

    try:
        buffer = io.BytesIO()
        styles = getSampleStyleSheet()
        story = []
        subtitle = f'Supplier: {selected_supplier_name}'
        if date_from or date_to:
            subtitle += f' | Period: {date_from or "Start"} to {date_to or "Present"}'
        subtitle += f' | Total Bills: {totals["bill_count"] or 0}'
        subtitle += f' | Billed: Rs.{total_billed:.2f} | Given: Rs.{total_given:.2f} | Pending: Rs.{total_pending:.2f}'

        _pdf_header(story, styles, 'Supplier Bill & Payment Report', subtitle)

        data = [['Bill No.', 'PO No.', 'Date', 'Supplier', 'Items', 'Total (Rs.)', 'Given (Rs.)', 'Pending (Rs.)', 'Status']]
        for o in orders:
            items_summary = ", ".join([f"{it.product.name} ({it.quantity})" for it in o.items.all()[:2]])
            if o.items.count() > 2:
                items_summary += f" +{o.items.count() - 2} more"
            if not items_summary:
                items_summary = "-"

            if o.paid_amount >= o.total_amount:
                pay_status = 'Paid'
            elif o.paid_amount > 0:
                pay_status = 'Partial'
            else:
                pay_status = 'Unpaid'

            data.append([
                o.bill_number or '-',
                o.order_number,
                str(o.order_date),
                o.supplier.company_name[:20],
                items_summary[:30],
                f'{o.total_amount:.2f}',
                f'{o.paid_amount:.2f}',
                f'{o.balance_amount:.2f}',
                pay_status,
            ])

        story.append(_make_pdf_table(data))
        _build_pdf(story, buffer, landscape_mode=True)
        filename = f'supplier_report_{timezone.now().strftime("%Y%m%d_%H%M")}.pdf'
        return _pdf_response(buffer, filename)

    except ImportError:
        messages.error(request, 'ReportLab not installed.')
        return redirect('reports:suppliers')


@login_required
def supplier_report_csv(request):
    if not request.user.is_manager:
        return HttpResponse('Unauthorized', status=401)

    from suppliers.models import Supplier
    from purchase.models import PurchaseOrder

    supplier_id = request.GET.get('supplier', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    payment_status = request.GET.get('payment_status', '')
    q = request.GET.get('q', '').strip()

    orders = PurchaseOrder.objects.all().select_related('supplier').prefetch_related('items__product').order_by('-order_date', '-id')

    if supplier_id:
        try:
            supplier_obj = Supplier.objects.get(pk=supplier_id)
            orders = orders.filter(supplier=supplier_obj)
        except (Supplier.DoesNotExist, ValueError):
            pass

    if date_from:
        orders = orders.filter(order_date__gte=date_from)
    if date_to:
        orders = orders.filter(order_date__lte=date_to)

    if q:
        orders = orders.filter(
            Q(bill_number__icontains=q) |
            Q(order_number__icontains=q) |
            Q(supplier__company_name__icontains=q) |
            Q(notes__icontains=q)
        )

    if payment_status == 'paid':
        orders = orders.filter(paid_amount__gte=F('total_amount'))
    elif payment_status == 'partial':
        orders = orders.filter(paid_amount__gt=0, paid_amount__lt=F('total_amount'))
    elif payment_status == 'unpaid':
        orders = orders.filter(paid_amount=0)

    response = HttpResponse(content_type='text/csv')
    filename = f'supplier_report_{timezone.now().strftime("%Y%m%d_%H%M")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'Bill / Invoice Number', 'Purchase Order Number', 'Date',
        'Supplier Company', 'Contact Person', 'Phone', 'GST Number',
        'Items Details', 'Total Amount', 'Given Payment (Paid)',
        'Pending Payment (Balance)', 'Payment Status', 'Order Status'
    ])

    for o in orders:
        items_detail = "; ".join([f"{it.product.name} (Qty: {it.quantity}, Rate: {it.purchase_price})" for it in o.items.all()])
        if o.paid_amount >= o.total_amount:
            pay_status = 'Paid'
        elif o.paid_amount > 0:
            pay_status = 'Partially Paid'
        else:
            pay_status = 'Unpaid'

        writer.writerow([
            o.bill_number or '',
            o.order_number,
            o.order_date.isoformat() if o.order_date else '',
            o.supplier.company_name,
            o.supplier.contact_person,
            o.supplier.phone,
            o.supplier.gst_number or '',
            items_detail,
            float(o.total_amount),
            float(o.paid_amount),
            float(o.balance_amount),
            pay_status,
            o.get_status_display(),
        ])

    return response


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
