"""
Base settings for ogani-e-commerce-site project.
Shared across all environments.
"""

from pathlib import Path
import os
from decouple import config
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to root repository directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-key-change-in-production')

# Application definition
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Internal domain apps
    'apps.home.apps.HomeConfig',
    'apps.product.apps.ProductConfig',
    'apps.cart.apps.CartConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.blog.apps.BlogConfig',
    'apps.contact.apps.ContactConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.review.apps.ReviewConfig',
    
    'django.contrib.sites',
    
    # Third-party plugins
    'ckeditor',
    'ckeditor_uploader',
    'paypal.standard.ipn',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

UNFOLD = {
    "SITE_TITLE": "Ogani Admin",
    "SITE_HEADER": "Ogani Dashboard",
    "SITE_SUBHEADER": "E-Commerce Management System",
    "SITE_SYMBOL": "shopping_cart", # Material symbol icon
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME": "dark", # dark, light, or auto
    "COLORS": {
        "primary": {
            "50": "240 253 244",
            "100": "220 252 231",
            "200": "187 247 208",
            "300": "134 239 172",
            "400": "74 222 128",
            "500": "34 197 94",
            "600": "22 163 74",
            "700": "21 128 61",
            "800": "22 101 52",
            "900": "20 83 45",
            "950": "5 46 22",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Store Management",
                "separator": True,
                "items": [
                    {
                        "title": "Products",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:product_product_changelist"),
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:product_productcategory_changelist"),
                    },
                    {
                        "title": "Product Reviews",
                        "icon": "star",
                        "link": reverse_lazy("admin:review_productreview_changelist"),
                    },
                ],
            },
            {
                "title": "Orders & Sales",
                "separator": True,
                "items": [
                    {
                        "title": "Purchase History",
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:payment_purchasehistory_changelist"),
                    },
                    {
                        "title": "Shopping Carts",
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:cart_cartid_changelist"),
                    },
                    {
                        "title": "Cart Items",
                        "icon": "shopping_bag",
                        "link": reverse_lazy("admin:cart_cartproduct_changelist"),
                    },
                    {
                        "title": "Wishlists",
                        "icon": "favorite",
                        "link": reverse_lazy("admin:cart_userwishlist_changelist"),
                    },
                ],
            },
            {
                "title": "Users & Content",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "group",
                        "link": reverse_lazy("admin:accounts_useraccount_changelist"),
                    },
                    {
                        "title": "Blog Posts",
                        "icon": "article",
                        "link": reverse_lazy("admin:blog_blogmodel_changelist"),
                    },
                    {
                        "title": "Blog Categories",
                        "icon": "label",
                        "link": reverse_lazy("admin:blog_blogcategory_changelist"),
                    },
                    {
                        "title": "Blog Comments",
                        "icon": "comment",
                        "link": reverse_lazy("admin:blog_blogcommentmodel_changelist"),
                    },
                    {
                        "title": "Contact Messages",
                        "icon": "mail",
                        "link": reverse_lazy("admin:contact_contactformmodel_changelist"),
                    },
                    {
                        "title": "Newsletter Subscribers",
                        "icon": "mark_email_unread",
                        "link": reverse_lazy("admin:contact_newslettermodel_changelist"),
                    },
                ],
            },
        ],
    },
}

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_ADAPTER = 'apps.accounts.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.accounts.adapters.CustomSocialAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                # Custom context processors
                'common.context_processors.cart_product_count.product_in_cart_count',
                'common.context_processors.wishlist_tracker.wishlist_counter',
                'common.context_processors.money_counter.cart_total',
                'common.context_processors.money_counter.cart_total_without_tax',
                'common.context_processors.make_newsletter_form_available.newsletter_for_all_app',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom Authentication User Model
AUTH_USER_MODEL = 'accounts.UserAccount'

# CKEditor config
CKEDITOR_UPLOAD_PATH = "uploads/"

# PayPal REST API settings
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID', default='')
PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET', default='')
PAYPAL_MODE = config('PAYPAL_MODE', default='sandbox')

# Email settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Session Cookie Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1209600  # 14 days

