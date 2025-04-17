import os
from pathlib import Path
import dj_database_url
import psycopg2  # Import psycopg2 for database connection
import dj_database_url
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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # This should be second
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

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
    'default': dj_database_url.config(
        default='postgresql://depar_info_user:D4780OeesktIxMLMZyZmVLyA5ryqJuYo@dpg-cvvuttjuibrs73bqmifg-a/dep_info',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_USER_MODEL = 'accounts.User'  # Add back the AUTH_USER_MODEL setting

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

#
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'department-info.onrender.com']

# Use environment variables for sensitive data
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')


# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Enable WhiteNoise compression and caching support
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



