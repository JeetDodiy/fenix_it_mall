#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py cleanup_duplicate_products || true
python manage.py migrate
python manage.py init_admin
python manage.py loaddata initial_catalog.json || true
