from django.urls import path
from django.views.generic import TemplateView
from products.models import Product

app_name = 'core'

class LandingView(TemplateView):
    template_name = 'core/landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['features'] = [
            "Real-time Inventory Tracking",
            "Advanced Point of Sale (POS)",
            "Purchase Order Management",
            "Supplier & Customer Profiles",
            "Employee & Attendance Management",
            "Comprehensive Analytics Dashboard"
        ]
        context['modules'] = [
            {'icon': '📦', 'name': 'Inventory', 'desc': 'Track stock, adjustments, and movements.'},
            {'icon': '🛒', 'name': 'POS & Sales', 'desc': 'Quick checkout with barcode scanning.'},
            {'icon': '🚚', 'name': 'Purchases', 'desc': 'Manage suppliers and reorder stock.'},
            {'icon': '👥', 'name': 'Customers', 'desc': 'Manage clients and track loyalty.'},
            {'icon': '👨‍💼', 'name': 'HR Module', 'desc': 'Employee attendance and salaries.'},
            {'icon': '📊', 'name': 'Reports', 'desc': 'Detailed reports and data exports.'},
        ]
        context['tech_stack'] = ['Django 5', 'Python 3.13', 'SQLite', 'Tailwind', 'Three.js', 'Chart.js', 'Alpine.js', 'GSAP']
        return context

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
]
