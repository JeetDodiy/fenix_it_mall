#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py cleanup_duplicate_products || true
python manage.py clean_test_data || true
python manage.py migrate

python manage.py init_admin
# Demo data seeding disabled to keep store clean
# python manage.py loaddata initial_catalog.json || true
# python manage.py seed_store_catalog || true
