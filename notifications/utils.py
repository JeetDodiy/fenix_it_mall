"""
Notifications Utility – Stock Alert Helpers
Called from sales, inventory, and any view that modifies stock quantities.
"""
from .models import Notification


def create_stock_notification(product, triggered_by_user=None):
    """
    Check a product's stock level and create a Notification if needed.

    - Zero stock  → 'out_of_stock' alert (type: low_stock)
    - Low stock   → 'low_stock'     alert (type: low_stock)
    - Normal stock → nothing

    Duplicate suppression: if an unread notification for the same product
    and the same alert title already exists, a new one is NOT created.
    """
    if product.stock_quantity <= 0:
        title = f'Out of Stock: {product.name}'
        message = (
            f'"{product.name}" ({product.product_code}) is now OUT OF STOCK. '
            f'Please reorder immediately.'
        )
    elif product.stock_quantity <= product.low_stock_threshold:
        title = f'Low Stock Alert: {product.name}'
        message = (
            f'"{product.name}" ({product.product_code}) has only '
            f'{product.stock_quantity} unit(s) remaining '
            f'(threshold: {product.low_stock_threshold}). Consider restocking.'
        )
    else:
        # Stock is fine – nothing to notify
        return

    link = f'/inventory/'

    # Suppress duplicates: skip if unread notification with same title exists
    already_exists = Notification.objects.filter(
        title=title,
        is_read=False,
        notification_type='low_stock',
    ).exists()

    if already_exists:
        return

    # Create notification – user=None makes it visible to all admin/managers
    # via the global context processor (which fetches user=None ones too)
    Notification.objects.create(
        title=title,
        message=message,
        notification_type='low_stock',
        link=link,
        user=triggered_by_user,  # associate with the user who triggered it
        is_read=False,
    )
