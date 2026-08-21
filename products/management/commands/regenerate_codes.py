"""
Management command to regenerate barcode and QR code images for all products
"""
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Regenerate barcode and QR code images for all products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--product-id',
            type=int,
            help='Regenerate for a specific product ID only',
        )

    def handle(self, *args, **options):
        product_id = options.get('product_id')
        
        if product_id:
            products = Product.objects.filter(pk=product_id)
            if not products.exists():
                self.stdout.write(self.style.ERROR(f'Product with ID {product_id} not found'))
                return
        else:
            products = Product.objects.all()
        
        total = products.count()
        self.stdout.write(f'Regenerating codes for {total} product(s)...')
        
        success_count = 0
        error_count = 0
        
        for product in products:
            try:
                # Clear existing images
                if product.barcode_image:
                    product.barcode_image.delete(save=False)
                if product.qr_code:
                    product.qr_code.delete(save=False)
                
                product.barcode_image = None
                product.qr_code = None
                product.save()
                
                # Check if images were generated
                product.refresh_from_db()
                if product.barcode_image and product.qr_code:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {product.name} ({product.product_code})')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ {product.name} - Images not generated')
                    )
                    error_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ {product.name} - Error: {str(e)}')
                )
                error_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Success: {success_count}'))
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f'Errors: {error_count}'))
        self.stdout.write('Done!')
