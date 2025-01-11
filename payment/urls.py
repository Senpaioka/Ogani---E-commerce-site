from django.urls import path
from payment import views


app_name = 'payment'


urlpatterns = [
    path('checkout/', views.checkout_page, name='checkout'),
]
