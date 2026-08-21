"""
Management command to fix purchase order status inconsistencies
"""
from django.core.management.base import BaseCommand
from purchase.models import PurchaseOrder


class Command(BaseCommand):
    help = 'Fix purchase order status based on actual received quantities'

    def handle(self, *args, **options):
        orders = PurchaseOrder.objects.all()
        fixed_count = 0
        
        self.stdout.write('Checking all purchase orders...\n')
        
        for order in orders:
            items = order.items.all()
            if not items:
                continue
            
            total_ordered = sum(item.quantity for item in items)
            total_received = sum(item.received_quantity for item in items)
            
            # Determine correct status
            if total_received == 0:
                correct_status = 'pending'
            elif total_received >= total_ordered:
                correct_status = 'received'
            else:
                correct_status = 'partial'
            
            # Update if wrong
            if order.status != correct_status:
                old_status = order.status
                order.status = correct_status
                order.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {order.order_number}: {old_status} → {correct_status} '
                        f'(Received: {total_received}/{total_ordered})'
                    )
                )
                fixed_count += 1
            else:
                self.stdout.write(
                    f'  {order.order_number}: {order.status} (OK - {total_received}/{total_ordered})'
                )
        
        self.stdout.write('')
        if fixed_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} purchase order(s)'))
        else:
            self.stdout.write(self.style.SUCCESS('All purchase orders are consistent!'))
