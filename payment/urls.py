from django.urls import path, include
from payment import views


app_name = 'payment'


urlpatterns = [
    path('checkout/', views.checkout_page, name='checkout'),
    path('successful/', views.payment_success_view, name='payment_successful'),
    path('failed/', views.payment_failed_view, name='payment_failed'),
]
