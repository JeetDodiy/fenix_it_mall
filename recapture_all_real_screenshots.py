import os
import time
from playwright.sync_api import sync_playwright

os.makedirs('pdf_report_assets', exist_ok=True)

def capture_all_proper_screens():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1366, 'height': 768})
        page = context.new_page()

        # 1. Login Page (public)
        print("Capturing screen_01_login.png...")
        page.goto('http://127.0.0.1:8000/accounts/login/', wait_until='networkidle')
        page.wait_for_timeout(1000)
        page.screenshot(path='pdf_report_assets/screen_01_login.png')

        # 2. Register Page (public)
        print("Capturing screen_02_register.png...")
        page.goto('http://127.0.0.1:8000/accounts/register/', wait_until='networkidle')
        page.wait_for_timeout(1000)
        page.screenshot(path='pdf_report_assets/screen_02_register.png')

        # Now Perform Login with admin / admin123
        print("Logging in with admin / admin123...")
        page.goto('http://127.0.0.1:8000/accounts/login/', wait_until='networkidle')
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('button[type="submit"]')
        page.wait_for_url('**/dashboard/**', timeout=10000)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1500)
        print(f"Logged in successfully! Current URL: {page.url}")

        # Authenticated Routes
        auth_routes = [
            ('screen_03_dashboard_light.png', 'http://127.0.0.1:8000/dashboard/'),
            ('screen_04_recent_activity.png', 'http://127.0.0.1:8000/dashboard/recent/'),
            ('screen_05_user_list.png', 'http://127.0.0.1:8000/accounts/users/'),
            ('screen_06_admin_pwd.png', 'http://127.0.0.1:8000/accounts/password/'),
            ('screen_07_profile.png', 'http://127.0.0.1:8000/accounts/profile/'),
            ('screen_08_pos_terminal.png', 'http://127.0.0.1:8000/sales/pos/'),
            ('screen_09_products_list.png', 'http://127.0.0.1:8000/products/'),
            ('screen_10_product_form.png', 'http://127.0.0.1:8000/products/add/'),
            ('screen_11_categories.png', 'http://127.0.0.1:8000/products/categories/'),
            ('screen_12_brands.png', 'http://127.0.0.1:8000/products/brands/'),
            ('screen_13_purchase_orders.png', 'http://127.0.0.1:8000/purchase/'),
            ('screen_14_purchase_create.png', 'http://127.0.0.1:8000/purchase/add/'),
            ('screen_15_supplier_report.png', 'http://127.0.0.1:8000/reports/suppliers/'),
            ('screen_16_settings.png', 'http://127.0.0.1:8000/settings/'),
            ('screen_17_attendance.png', 'http://127.0.0.1:8000/employees/attendance/'),
            ('screen_18_leaves.png', 'http://127.0.0.1:8000/employees/leaves/'),
            ('screen_19_employees.png', 'http://127.0.0.1:8000/employees/'),
            ('screen_20_customers.png', 'http://127.0.0.1:8000/customers/'),
            ('screen_21_reports_hub.png', 'http://127.0.0.1:8000/reports/sales/'),
        ]

        for fname, url in auth_routes:
            print(f"Capturing {fname} from {url}...")
            try:
                page.goto(url, wait_until='networkidle')
                page.wait_for_timeout(1000)
                # Ensure we are not redirected to login
                if '/accounts/login/' in page.url:
                    print(f"WARNING: {fname} was redirected to login!")
                else:
                    print(f"SUCCESS: {fname} loaded URL {page.url}")
                page.screenshot(path=os.path.join('pdf_report_assets', fname))
            except Exception as e:
                print(f"Failed {fname}: {e}")

        # Also capture POS search and cart if needed
        print("Capturing POS search...")
        try:
            page.goto('http://127.0.0.1:8000/sales/pos/', wait_until='networkidle')
            page.wait_for_timeout(1000)
            page.fill('input#pos-search', 'Dell')
            page.wait_for_timeout(800)
            page.screenshot(path='docs_assets/screenshot_pos_search.png')
            print("Captured docs_assets/screenshot_pos_search.png")
        except Exception as e:
            print(f"Failed POS search: {e}")

        print("Capturing POS terminal full...")
        try:
            page.goto('http://127.0.0.1:8000/sales/pos/', wait_until='networkidle')
            page.wait_for_timeout(1000)
            page.screenshot(path='docs_assets/screenshot_pos_terminal.png')
            print("Captured docs_assets/screenshot_pos_terminal.png")
        except Exception as e:
            print(f"Failed POS terminal: {e}")

        print("Capturing Sales Invoices list...")
        try:
            page.goto('http://127.0.0.1:8000/sales/', wait_until='networkidle')
            page.wait_for_timeout(1000)
            page.screenshot(path='docs_assets/screenshot_sales_invoices.png')
            print("Captured docs_assets/screenshot_sales_invoices.png")
        except Exception as e:
            print(f"Failed Sales Invoices: {e}")

        browser.close()
        print("All proper screenshots captured successfully!")

if __name__ == '__main__':
    capture_all_proper_screens()
