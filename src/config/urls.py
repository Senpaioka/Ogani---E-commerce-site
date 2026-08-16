from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # Core Application Routes with App Namespacing
    path('', include('apps.home.urls', namespace='home')),
    path('products/', include('apps.product.urls', namespace='product')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('blogs/', include('apps.blog.urls', namespace='blog')),
    path('contact/', include('apps.contact.urls', namespace='contact')),
    path('payments/', include('apps.payment.urls', namespace='payment')),
    path('reviews/', include('apps.review.urls', namespace='review')),

    # Third-Party Packages
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('accounts/', include('allauth.urls')),
]


# Static and Media file serving in local development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore[arg-type]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore[arg-type]

                