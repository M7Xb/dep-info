import os
from pathlib import Path
import dj_database_url
import psycopg2  # Import psycopg2 for database connection

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'admin_dashboard.apps.AdminDashboardConfig',  # Make sure this is here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add these settings
CSRF_COOKIE_SECURE = True  # for HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('postgresql://dep_info_user:D4780OeesktIxMLMZyZmVLyA5ryqJuYo@dpg-cvvuttjuibrs73bqmifg-a/dep_info'))
}

AUTH_USER_MODEL = 'accounts.User'  # Add back the AUTH_USER_MODEL setting

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Add these basic settings as well
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-app-name.onrender.com']

# Use environment variables for sensitive data
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')


# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Test database connection
try:
    conn = psycopg2.connect(
        dbname="dep-info",
        user="postgres",
        password="admin123",
        host="localhost",
        port="5432"
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")



