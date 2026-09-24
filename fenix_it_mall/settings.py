"""
Fenix IT Mall – Django Settings
Production-quality IT Shop Management System
"""

from pathlib import Path
import os

# Auto-clean Cloudinary environment variable if pasted with quotes or 'CLOUDINARY_URL=' prefix
if 'CLOUDINARY_URL' in os.environ:
    val = os.environ['CLOUDINARY_URL'].strip()
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        val = val[1:-1].strip()
    if 'CLOUDINARY_URL=' in val:
        val = val.split('CLOUDINARY_URL=', 1)[1].strip()
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        val = val[1:-1].strip()
    if val.startswith('cloudinary://'):
        os.environ['CLOUDINARY_URL'] = val
    else:
        del os.environ['CLOUDINARY_URL']

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fenix-it-mall-bca-project-2024-secret-key-change-in-production')

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    # Fenix IT Mall Apps
    'core',
    'accounts',
    'dashboard',
    'products',
    'inventory',
    'sales',
    'purchase',
    'customers',
    'suppliers',
    'employees',
    'reports',
    'notifications',
    'settings_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.up.railway.app',
    'https://*.pythonanywhere.com',
    'http://127.0.0.1',
    'http://localhost',
]

ROOT_URLCONF = 'fenix_it_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.notifications_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'fenix_it_mall.wsgi.application'

# Database configuration (Supports persistent PostgreSQL via DATABASE_URL on Render, or SQLite by default)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Storage configuration: Persistent Cloudinary for cloud (Render) or local FileSystem
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

if CLOUDINARY_CLOUD_NAME or CLOUDINARY_URL:
    import urllib.parse
    CLOUDINARY_STORAGE = {}
    if CLOUDINARY_URL:
        # Support full URL: cloudinary://API_KEY:API_SECRET@CLOUD_NAME
        clean_url = CLOUDINARY_URL.replace('CLOUDINARY_URL=', '').strip()
        parsed = urllib.parse.urlparse(clean_url)
        CLOUDINARY_STORAGE['CLOUD_NAME'] = parsed.hostname
        CLOUDINARY_STORAGE['API_KEY'] = parsed.username
        CLOUDINARY_STORAGE['API_SECRET'] = parsed.password
    else:
        CLOUDINARY_STORAGE['CLOUD_NAME'] = CLOUDINARY_CLOUD_NAME
        CLOUDINARY_STORAGE['API_KEY'] = os.environ.get('CLOUDINARY_API_KEY')
        CLOUDINARY_STORAGE['API_SECRET'] = os.environ.get('CLOUDINARY_API_SECRET')

    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

# Media files (product images, logos, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Authentication redirects
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Message tags for toast styling
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# File upload size limit: 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
