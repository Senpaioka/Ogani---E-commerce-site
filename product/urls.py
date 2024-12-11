from django.urls import path
from product import views


app_name = 'product'

urlpatterns = [
    path('store/', views.product_store_page, name='store_page'),
    path('product_page/<int:product_id>/', views.single_product_page, name='single_product'),
    path('category_product/<str:category_name>/', views.product_by_category_page, name='category_page'),
]
