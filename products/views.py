"""
Products App – Views for Product, Category, Brand CRUD
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Product, Category, Brand, ProductImage
from .forms import ProductForm, CategoryForm, BrandForm, ProductImageForm


# ─── Product Views ───

@login_required
def product_list(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    status = request.GET.get('status', '')
    sort = request.GET.get('sort', '-created_at')

    products = Product.objects.filter(is_active=True).select_related('category', 'brand')

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(product_code__icontains=q) | Q(barcode_number__icontains=q)
        )
    if category:
        products = products.filter(category_id=category)
    if brand:
        products = products.filter(brand_id=brand)
    if status:
        products = products.filter(status=status)

    products = products.order_by(sort)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    return render(request, 'products/list.html', {
        'products': products_page,
        'categories': categories,
        'brands': brands,
        'q': q,
        'selected_category': category,
        'selected_brand': brand,
        'selected_status': status,
        'total_count': products.count(),
    })


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


@login_required
def product_add(request):
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('products:list')

    form = ProductForm(request.POST or None)
    image_form = ProductImageForm(request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        product = form.save()
        # Handle multiple images
        for f in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=f)
        messages.success(request, f'Product "{product.name}" added successfully!')
        return redirect('products:detail', pk=product.pk)

    return render(request, 'products/form.html', {
        'form': form,
        'image_form': image_form,
        'title': 'Add Product',
        'action': 'Add',
    })


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('products:list')

    form = ProductForm(request.POST or None, instance=product)
    image_form = ProductImageForm(request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        product = form.save()
        for f in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=f)
        messages.success(request, f'Product "{product.name}" updated successfully!')
        return redirect('products:detail', pk=product.pk)

    return render(request, 'products/form.html', {
        'form': form,
        'image_form': image_form,
        'product': product,
        'title': f'Edit Product – {product.name}',
        'action': 'Update',
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_admin:
        messages.error(request, 'Permission denied.')
        return redirect('products:list')
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, f'Product "{product.name}" deleted.')
        return redirect('products:list')
    return redirect('products:list')


@login_required
def product_barcode(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/barcode.html', {'product': product})


@login_required
def product_qrcode(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/qrcode.html', {'product': product})


@login_required
def product_search_ajax(request):
    """AJAX search by barcode or name"""
    q = request.GET.get('q', '')
    barcode = request.GET.get('barcode', '')

    if barcode:
        product = Product.objects.filter(
            Q(barcode_number=barcode) | Q(product_code=barcode), is_active=True
        ).first()
        if product:
            return JsonResponse({'product': {
                'id': product.pk,
                'name': product.name,
                'selling_price': str(product.selling_price),
                'stock_quantity': product.stock_quantity,
                'product_code': product.product_code,
                'gst_percentage': str(product.gst_percentage),
            }})
        return JsonResponse({'product': None})

    products = Product.objects.filter(
        Q(name__icontains=q) | Q(product_code__icontains=q),
        is_active=True, stock_quantity__gt=0
    )[:10]

    return JsonResponse({'products': [
        {'id': p.pk, 'name': p.name, 'selling_price': str(p.selling_price),
         'stock_quantity': p.stock_quantity, 'product_code': p.product_code,
         'gst_percentage': str(p.gst_percentage)}
        for p in products
    ]})


# ─── Category Views ───

@login_required
def category_list(request):
    q = request.GET.get('q', '')
    categories = Category.objects.all()
    if q:
        categories = categories.filter(name__icontains=q)
    paginator = Paginator(categories, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'products/category_list.html', {'categories': page, 'q': q})


@login_required
def category_add(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Category added successfully!')
        return redirect('products:category_list')
    return render(request, 'products/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Category updated!')
        return redirect('products:category_list')
    return render(request, 'products/category_form.html', {'form': form, 'title': 'Edit Category', 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('products:category_list')
    return redirect('products:category_list')


# ─── Brand Views ───

@login_required
def brand_list(request):
    q = request.GET.get('q', '')
    brands = Brand.objects.all()
    if q:
        brands = brands.filter(name__icontains=q)
    paginator = Paginator(brands, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'products/brand_list.html', {'brands': page, 'q': q})


@login_required
def brand_add(request):
    form = BrandForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Brand added successfully!')
        return redirect('products:brand_list')
    return render(request, 'products/brand_form.html', {'form': form, 'title': 'Add Brand'})


@login_required
def brand_edit(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    form = BrandForm(request.POST or None, request.FILES or None, instance=brand)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Brand updated!')
        return redirect('products:brand_list')
    return render(request, 'products/brand_form.html', {'form': form, 'title': 'Edit Brand', 'brand': brand})


@login_required
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted.')
        return redirect('products:brand_list')
    return redirect('products:brand_list')


@login_required
def regenerate_barcode_qr(request, pk):
    """Regenerate barcode and QR code for a product"""
    product = get_object_or_404(Product, pk=pk)
    if not request.user.is_manager:
        messages.error(request, 'Permission denied.')
        return redirect('products:detail', pk=pk)
    
    if request.method == 'POST':
        # Clear existing images
        if product.barcode_image:
            product.barcode_image.delete(save=False)
        if product.qr_code:
            product.qr_code.delete(save=False)
        
        product.barcode_image = None
        product.qr_code = None
        product.save()  # This will trigger regeneration
        
        messages.success(request, f'Barcode and QR code regenerated for "{product.name}"')
        return redirect('products:detail', pk=pk)
    
    return redirect('products:detail', pk=pk)
