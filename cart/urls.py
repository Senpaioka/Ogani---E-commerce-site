from django.urls import path
from cart import views


app_name = 'cart'


urlpatterns = [
    # cart link
    path('cart_page/', views.main_cart_page, name='cart_page'),
    path('add_cart/<int:product_id>/', views.add_product_into_cart, name='add_cart'),
    path('increase_quantity/<int:product_id>/', views.increase_product_quantity, name='increase_product'),
    path('decrease_quantity/<int:product_id>/', views.decrease_product_quantity, name='decrease_product'),
    path('delete_product/<int:product_id>/', views.delete_cart_product, name='delete_product'),
    # wishlist link
    path('wishlist/', views.wishlist_main_page, name='wishlist_page'),
    path('add_to_wishlist/<int:product_id>/', views.wishlist_add_product, name='add_wishlist'),
    path('remove_wishlist/<int:product_id>/', views.remove_wishlist_product, name='remove_wishlist'),
]


