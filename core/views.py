"""
Core App – Views: Landing page, 404, 500
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    modules = [
        {'icon': '📦', 'name': 'Product Management',       'desc': 'Manage your full IT product catalog with categories, brands, barcodes, and QR codes.'},
        {'icon': '🛒', 'name': 'POS / Sales',              'desc': 'Fast point-of-sale system with invoice generation, GST calculation, and customer management.'},
        {'icon': '🏭', 'name': 'Inventory Control',        'desc': 'Track stock levels, receive alerts for low stock, and log every movement in real time.'},
        {'icon': '📋', 'name': 'Purchase Orders',          'desc': 'Create and track purchase orders from suppliers with full order history.'},
        {'icon': '👥', 'name': 'Customer Management',      'desc': 'Maintain customer records, purchase history, and contact details in one place.'},
        {'icon': '🏢', 'name': 'Supplier Management',      'desc': 'Manage supplier profiles, contacts, and link products directly to suppliers.'},
        {'icon': '👷', 'name': 'Employee Management',      'desc': 'Track staff details, attendance, roles, and performance within your shop.'},
        {'icon': '📊', 'name': 'Reports & Analytics',      'desc': 'Visual dashboards and detailed reports for sales, revenue, profit, and inventory trends.'},
        {'icon': '🔔', 'name': 'Smart Notifications',      'desc': 'Instant in-app alerts for low stock, new orders, and important business events.'},
    ]

    tech_stack = [
        '🐍 Python 3', '🟩 Django 5', '🗄️ SQLite / PostgreSQL',
        '📊 Chart.js', '🎬 Three.js', '⚡ GSAP',
        '📱 Responsive CSS', '🏷️ Barcode / QR Code', '📄 PDF Reports',
    ]

    return render(request, 'core/landing.html', {'modules': modules, 'tech_stack': tech_stack})


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)


def handler500(request):
    return render(request, 'core/500.html', status=500)


def handler403(request, exception):
    return render(request, 'core/403.html', status=403)
