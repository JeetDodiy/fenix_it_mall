import os
import time
from playwright.sync_api import sync_playwright

os.makedirs('pdf_report_assets', exist_ok=True)

def capture_screens():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1366, 'height': 768})
        page = context.new_page()

        # Log in as Admin
        page.goto('http://127.0.0.1:8000/accounts/login/')
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)

        routes = [
            ('screen_09_products_list.png', 'http://127.0.0.1:8000/products/'),
            ('screen_10_product_form.png', 'http://127.0.0.1:8000/products/create/'),
            ('screen_11_categories.png', 'http://127.0.0.1:8000/products/categories/'),
            ('screen_12_brands.png', 'http://127.0.0.1:8000/products/brands/'),
            ('screen_13_purchase_orders.png', 'http://127.0.0.1:8000/purchase/'),
            ('screen_14_purchase_create.png', 'http://127.0.0.1:8000/purchase/create/'),
            ('screen_15_supplier_report.png', 'http://127.0.0.1:8000/reports/suppliers/'),
            ('screen_16_settings.png', 'http://127.0.0.1:8000/settings/'),
            ('screen_17_attendance.png', 'http://127.0.0.1:8000/employees/attendance/'),
            ('screen_18_leaves.png', 'http://127.0.0.1:8000/employees/leaves/'),
            ('screen_19_employees.png', 'http://127.0.0.1:8000/employees/'),
            ('screen_20_customers.png', 'http://127.0.0.1:8000/customers/'),
            ('screen_21_reports_hub.png', 'http://127.0.0.1:8000/reports/'),
        ]

        for fname, url in routes:
            print(f"Capturing {fname} from {url}...")
            try:
                page.goto(url, wait_until='networkidle')
                page.wait_for_timeout(1000)
                page.screenshot(path=os.path.join('pdf_report_assets', fname))
            except Exception as e:
                print(f"Failed {fname}: {e}")

        browser.close()
        print("Batch capture completed!")

if __name__ == '__main__':
    capture_screens()
