from django.urls import path
from product import views


app_name = 'product'

urlpatterns = [
    path('store/', views.product_store_page, name='store_page'),
    path('product_page/', views.single_product_page, name='single_product'),
]
