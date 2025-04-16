import os
from pathlib import Path

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'project_db',
        'USER': 'root',
        'PASSWORD': 'mouad123',  # Use the password you set during installation
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_USER_MODEL = 'accounts.User'  # Add back the AUTH_USER_MODEL setting

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Add these basic settings as well
DEBUG = False
ALLOWED_HOSTS = ['your-app-name.onrender.com']  # Replace with your Render app URL

# Use environment variables for sensitive data
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')


if not os.environ.get('DJANGO_SKIP_DB_CREATE', False):
    try:
        from .db_utils import create_database_if_not_exists
        create_database_if_not_exists()
    except Exception as e:
        print(f"Failed to create database: {e}")


# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


