"""Sales App - Views"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone

from .models import Sale, SaleItem, InvoiceAuditLog
from products.models import Product, Category
from customers.models import Customer
from notifications.utils import create_stock_notification


@login_required
def pos(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                customer_id = request.POST.get('customer_id') or None
                payment_method = request.POST.get('payment_method', 'cash')
                discount_pct = float(request.POST.get('discount_percentage', 0))
                amount_paid = float(request.POST.get('amount_paid', 0))
                product_ids = request.POST.getlist('product_id[]')
                quantities = request.POST.getlist('quantity[]')
                prices = request.POST.getlist('price[]')

                if not product_ids:
                    messages.error(request, 'Cart is empty.')
                    return redirect('sales:pos')

                customer = Customer.objects.filter(pk=customer_id).first() if customer_id else None
                subtotal = sum(float(p) * int(q) for p, q in zip(prices, quantities))
                discount_amount = round(subtotal * discount_pct / 100, 2)
                taxable = subtotal - discount_amount
                gst_amount = round(taxable * 0.18, 2)
                grand_total = round(taxable + gst_amount, 2)
                change_amount = max(0, amount_paid - grand_total)

                sale = Sale.objects.create(
                    customer=customer, created_by=request.user,
                    subtotal=subtotal, discount_percentage=discount_pct,
                    discount_amount=discount_amount, gst_amount=gst_amount,
                    grand_total=grand_total, amount_paid=amount_paid,
                    change_amount=change_amount, payment_method=payment_method,
                    status='completed',
                )

                from inventory.models import StockMovement
                for pid, qty, price in zip(product_ids, quantities, prices):
                    product = Product.objects.select_for_update().get(pk=pid)
                    qty_int = int(qty)
                    if product.stock_quantity < qty_int:
                        raise ValueError(
                            'Not enough stock for {}. Available: {}'.format(
                                product.name, product.stock_quantity))
                    SaleItem.objects.create(
                        sale=sale, product=product, quantity=qty_int,
                        unit_price=float(price),
                        gst_percentage=product.gst_percentage,
                        total_price=qty_int * float(price),
                    )
                    qty_before = product.stock_quantity
                    product.stock_quantity -= qty_int
                    product.save()
                    StockMovement.objects.create(
                        product=product, movement_type='out', quantity=qty_int,
                        quantity_before=qty_before,
                        quantity_after=product.stock_quantity,
                        reference='Sale: {}'.format(sale.invoice_number),
                        created_by=request.user,
                    )
                    create_stock_notification(product, triggered_by_user=request.user)

                # Log creation in InvoiceAuditLog
                InvoiceAuditLog.objects.create(
                    sale=sale,
                    action='created',
                    user=request.user,
                    details='Invoice created via POS terminal. Total: ₹{}, Payment: {}'.format(
                        grand_total, sale.get_payment_method_display())
                )

                messages.success(
                    request, 'Sale {} completed! Total: Rs.{}'.format(
                        sale.invoice_number, grand_total))
                return redirect('sales:invoice', pk=sale.pk)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('sales:pos')

    products = Product.objects.filter(
        is_active=True, stock_quantity__gt=0
    ).select_related('category', 'brand').prefetch_related('images')
    categories = Category.objects.filter(is_active=True)
    customers = Customer.objects.filter(is_active=True).order_by('name')
    return render(request, 'sales/pos.html', {
        'products': products, 'categories': categories, 'customers': customers,
    })


@login_required
def sale_list(request):
    q = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    payment = request.GET.get('payment', '')
    status = request.GET.get('status', '')
    period = request.GET.get('period', '')

    sales = Sale.objects.select_related('customer', 'created_by').order_by('-created_at')

    today = timezone.now().date()
    if period == 'today':
        sales = sales.filter(sale_date__date=today)
    elif period == 'week':
        week_ago = today - timezone.timedelta(days=7)
        sales = sales.filter(sale_date__date__gte=week_ago)
    elif period == 'month':
        month_start = today.replace(day=1)
        sales = sales.filter(sale_date__date__gte=month_start)

    if q:
        sales = sales.filter(
            Q(invoice_number__icontains=q) | Q(customer__name__icontains=q))
    if date_from:
        sales = sales.filter(sale_date__date__gte=date_from)
    if date_to:
        sales = sales.filter(sale_date__date__lte=date_to)
    if payment:
        sales = sales.filter(payment_method=payment)
    if status:
        sales = sales.filter(status=status)

    total_revenue = (
        sales.filter(status__in=['completed', 'corrected']).aggregate(t=Sum('grand_total'))['t'] or 0)
    paginator = Paginator(sales, 15)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'sales/list.html', {
        'sales': page,
        'q': q,
        'date_from': date_from,
        'date_to': date_to,
        'selected_payment': payment,
        'selected_status': status,
        'selected_period': period,
        'total_revenue': total_revenue,
        'payment_methods': Sale.PAYMENT_METHODS,
        'status_choices': Sale.STATUS_CHOICES,
    })


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('customer', 'created_by', 'voided_by', 'corrected_by'), pk=pk)
    audit_logs = sale.audit_logs.select_related('user').order_by('-created_at')
    return render(request, 'sales/detail.html', {'sale': sale, 'audit_logs': audit_logs})


@login_required
def sale_create(request):
    return redirect('sales:pos')


@login_required
def sale_invoice(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    from settings_app.models import CompanySettings
    company = CompanySettings.get_settings()
    return render(request, 'sales/invoice.html', {'sale': sale, 'company': company})


@login_required
def sale_log_print(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    InvoiceAuditLog.objects.create(
        sale=sale,
        action='printed',
        user=request.user,
        details='Invoice printed by {}'.format(request.user.get_full_name() or request.user.username)
    )
    return HttpResponse('OK')


@login_required
def sale_invoice_pdf(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    from settings_app.models import CompanySettings
    company = CompanySettings.get_settings()

    # Log PDF download
    InvoiceAuditLog.objects.create(
        sale=sale,
        action='downloaded',
        user=request.user,
        details='PDF invoice downloaded by {}'.format(request.user.get_full_name() or request.user.username)
    )

    try:
        import io
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer)
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                topMargin=20*mm, bottomMargin=20*mm,
                                leftMargin=20*mm, rightMargin=20*mm)
        styles = getSampleStyleSheet()
        story = []

        cname = company.company_name if company else 'Fenix IT Mall'
        story.append(Paragraph(cname, ParagraphStyle(
            'ct', parent=styles['Heading1'], fontSize=18, alignment=TA_CENTER)))
        if company and company.address:
            story.append(Paragraph(
                company.address.replace('\n', ', '),
                ParagraphStyle('cs', parent=styles['Normal'],
                               fontSize=9, alignment=TA_CENTER)))
        if company and company.phone:
            story.append(Paragraph(
                'Ph: {}'.format(company.phone),
                ParagraphStyle('cp', parent=styles['Normal'],
                               fontSize=9, alignment=TA_CENTER)))

        if sale.status == 'voided':
            story.append(Spacer(1, 4*mm))
            story.append(Paragraph('*** VOIDED INVOICE ***', ParagraphStyle(
                'void_hdr', parent=styles['Heading2'], fontSize=14, textColor=colors.red, alignment=TA_CENTER)))

        story.append(Spacer(1, 5*mm))
        story.append(Paragraph('INVOICE - {}'.format(sale.invoice_number),
                                styles['Heading2']))
        story.append(Paragraph(
            'Date: {}'.format(sale.sale_date.strftime('%d %b %Y %I:%M %p')),
            styles['Normal']))
        story.append(Paragraph(
            'Status: {}'.format(sale.get_status_display().upper()),
            styles['Normal']))

        if sale.customer:
            story.append(Paragraph(
                'Customer: {} | {}'.format(sale.customer.name, sale.customer.phone),
                styles['Normal']))
        else:
            story.append(Paragraph('Customer: Walk-in Customer', styles['Normal']))

        story.append(Spacer(1, 5*mm))

        # Items Table
        data = [['#', 'Product', 'Qty', 'Unit Price', 'Total']]
        for i, item in enumerate(sale.items.select_related('product').all(), 1):
            data.append([
                str(i),
                item.product.name[:35],
                str(item.quantity),
                'Rs.{}'.format(item.unit_price),
                'Rs.{}'.format(item.total_price),
            ])

        tbl = Table(data, colWidths=[10*mm, 85*mm, 20*mm, 25*mm, 30*mm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 5*mm))

        totals = [
            ['', 'Subtotal:', 'Rs.{}'.format(sale.subtotal)],
            ['', 'Discount ({}%):'.format(sale.discount_percentage),
             '-Rs.{}'.format(sale.discount_amount)],
            ['', 'GST (18%):', 'Rs.{}'.format(sale.gst_amount)],
            ['', 'GRAND TOTAL:', 'Rs.{}'.format(sale.grand_total)],
            ['', 'Payment:', sale.get_payment_method_display()],
        ]
        tt = Table(totals, colWidths=[100*mm, 40*mm, 30*mm])
        tt.setStyle(TableStyle([
            ('FONTNAME', (1, 3), (2, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 3), (2, 3), 11),
            ('LINEABOVE', (1, 3), (2, 3), 1, colors.black),
            ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
        ]))
        story.append(tt)
        story.append(Spacer(1, 10*mm))
        story.append(Paragraph(
            'Thank you for your purchase!',
            ParagraphStyle('thx', parent=styles['Normal'],
                           alignment=TA_CENTER, fontSize=11)))

        doc.build(story)
        buf.seek(0)
        resp = HttpResponse(buf, content_type='application/pdf')
        resp['Content-Disposition'] = (
            'inline; filename="invoice_{}.pdf"'.format(sale.invoice_number))
        return resp

    except ImportError:
        messages.error(request, 'ReportLab not installed. Run: pip install reportlab')
        return redirect('sales:invoice', pk=pk)


@login_required
def sale_void(request, pk):
    """
    Void a sale invoice safely:
    - Restores inventory stock quantities
    - Records StockMovement audit trail
    - Marks Sale as 'voided' with reason, voided_by, voided_at
    - Preserves invoice record in database for audit compliance
    """
    if not request.user.is_manager:
        messages.error(request, 'Permission denied. Only managers and admins can void invoices.')
        return redirect('sales:detail', pk=pk)

    sale = get_object_or_404(Sale, pk=pk)

    if sale.status == 'voided':
        messages.warning(request, 'Invoice {} is already voided.'.format(sale.invoice_number))
        return redirect('sales:detail', pk=pk)

    if request.method == 'POST':
        reason_choice = request.POST.get('void_reason', 'Other').strip()
        custom_notes = request.POST.get('additional_notes', '').strip()
        full_reason = f"{reason_choice} - {custom_notes}" if custom_notes else reason_choice

        try:
            with transaction.atomic():
                from inventory.models import StockMovement
                # 1. Restore all product stock
                for item in sale.items.select_related('product').all():
                    product = item.product
                    qty_before = product.stock_quantity
                    product.stock_quantity += item.quantity
                    product.save()

                    StockMovement.objects.create(
                        product=product,
                        movement_type='in',
                        quantity=item.quantity,
                        quantity_before=qty_before,
                        quantity_after=product.stock_quantity,
                        reference='Voided Invoice: {}'.format(sale.invoice_number),
                        created_by=request.user,
                    )

                # 2. Update sale record to voided
                sale.status = 'voided'
                sale.void_reason = full_reason
                sale.voided_by = request.user
                sale.voided_at = timezone.now()
                sale.save()

                # 3. Create Audit Log
                InvoiceAuditLog.objects.create(
                    sale=sale,
                    action='voided',
                    user=request.user,
                    details='Invoice voided by {}. Reason: {}. Stock restored.'.format(
                        request.user.get_full_name() or request.user.username, full_reason
                    )
                )

                messages.success(
                    request,
                    'Invoice {} has been successfully voided. Inventory stock has been restored.'.format(sale.invoice_number)
                )
                return redirect('sales:detail', pk=sale.pk)

        except Exception as e:
            messages.error(request, f'Error voiding invoice: {str(e)}')
            return redirect('sales:detail', pk=sale.pk)

    return render(request, 'sales/void_confirm.html', {'sale': sale})


@login_required
def sale_edit(request, pk):
    """
    Allow admin/manager to edit/correct a completed sale invoice.
    Requires correction reason, safely reconciles inventory stock,
    and logs audit history.
    """
    if not request.user.is_manager:
        messages.error(request, 'Permission denied. Only managers and admins can edit invoices.')
        return redirect('sales:list')

    sale = get_object_or_404(Sale, pk=pk)

    if sale.status == 'voided':
        messages.error(request, 'Cannot edit a voided invoice.')
        return redirect('sales:detail', pk=pk)

    old_total = sale.grand_total

    if request.method == 'POST':
        reason_choice = request.POST.get('correction_reason', '').strip()
        custom_notes  = request.POST.get('additional_notes', '').strip()
        full_reason   = f"{reason_choice} - {custom_notes}" if custom_notes else reason_choice

        if not full_reason:
            messages.error(request, 'A reason for invoice correction is required.')
            return redirect('sales:edit', pk=pk)

        try:
            with transaction.atomic():
                customer_id = request.POST.get('customer_id') or None
                sale.customer = Customer.objects.filter(pk=customer_id).first() if customer_id else None
                sale.payment_method = request.POST.get('payment_method', sale.payment_method)
                sale.notes = request.POST.get('notes', '')
                discount_pct = float(request.POST.get('discount_percentage', 0))
                sale.discount_percentage = discount_pct

                # ── 1. Restore old stock before rebuilding items ──────────────
                from inventory.models import StockMovement
                for old_item in sale.items.select_related('product').all():
                    old_item.product.stock_quantity += old_item.quantity
                    old_item.product.save()
                sale.items.all().delete()

                # ── 2. Rebuild items from POST ────────────────────────────────
                product_ids = request.POST.getlist('product_id[]')
                quantities  = request.POST.getlist('quantity[]')
                prices      = request.POST.getlist('price[]')

                if not product_ids:
                    raise ValueError('Sale must have at least one item.')

                subtotal = 0
                for pid, qty, price in zip(product_ids, quantities, prices):
                    product = Product.objects.select_for_update().get(pk=pid)
                    qty_int   = int(qty)
                    price_val = float(price)
                    if product.stock_quantity < qty_int:
                        raise ValueError(
                            'Not enough stock for {}. Available: {}'.format(
                                product.name, product.stock_quantity))
                    SaleItem.objects.create(
                        sale=sale, product=product,
                        quantity=qty_int, unit_price=price_val,
                        gst_percentage=product.gst_percentage,
                        total_price=qty_int * price_val,
                    )
                    qty_before = product.stock_quantity
                    product.stock_quantity -= qty_int
                    product.save()
                    StockMovement.objects.create(
                        product=product, movement_type='out',
                        quantity=qty_int,
                        quantity_before=qty_before,
                        quantity_after=product.stock_quantity,
                        reference='Invoice Correction: {}'.format(sale.invoice_number),
                        created_by=request.user,
                    )
                    create_stock_notification(product, triggered_by_user=request.user)
                    subtotal += qty_int * price_val

                # ── 3. Recalculate totals ─────────────────────────────────────
                discount_amount = round(subtotal * discount_pct / 100, 2)
                taxable         = subtotal - discount_amount
                gst_amount      = round(taxable * 0.18, 2)
                grand_total     = round(taxable + gst_amount, 2)

                sale.subtotal          = subtotal
                sale.discount_amount   = discount_amount
                sale.gst_amount        = gst_amount
                sale.grand_total       = grand_total
                sale.amount_paid       = grand_total
                sale.change_amount     = 0
                sale.status            = 'corrected'
                sale.correction_reason = full_reason
                sale.corrected_by      = request.user
                sale.corrected_at      = timezone.now()
                sale.save()

                # ── 4. Audit Log ──────────────────────────────────────────────
                InvoiceAuditLog.objects.create(
                    sale=sale,
                    action='corrected',
                    user=request.user,
                    details='Invoice corrected by {}. Reason: {}. Old Total: ₹{} → New Total: ₹{}'.format(
                        request.user.get_full_name() or request.user.username,
                        full_reason, old_total, grand_total
                    )
                )

                messages.success(request, 'Invoice {} updated and correction logged.'.format(sale.invoice_number))
                return redirect('sales:detail', pk=sale.pk)

        except Exception as e:
            messages.error(request, str(e))

    # ── GET – prepare context ──────────────────────────────────────────────
    products  = Product.objects.filter(is_active=True).order_by('name')
    customers = Customer.objects.filter(is_active=True).order_by('name')
    return render(request, 'sales/edit.html', {
        'sale': sale,
        'products': products,
        'customers': customers,
        'payment_methods': Sale.PAYMENT_METHODS,
        'status_choices': Sale.STATUS_CHOICES,
    })


@login_required
def sale_delete(request, pk):
    """
    Non-destructive deprecation: redirect delete requests to void
    """
    messages.info(request, 'Completed invoices cannot be permanently deleted. You may void the invoice instead.')
    return redirect('sales:void', pk=pk)
