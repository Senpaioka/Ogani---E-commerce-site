from .base import *

DEBUG = False

RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default='')
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='ogani-e-commerce-site.onrender.com,localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Security Hardening
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', cast=bool, default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Production Database (PostgreSQL if DATABASE_URL provided, else fallback to SQLite)
# Developers can use dj-database-url if preferred
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
