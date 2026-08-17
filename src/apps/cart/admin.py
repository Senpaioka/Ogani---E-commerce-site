from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.cart.models import CartID, CartProduct, UserWishList, Coupon


@admin.register(CartID)
class CartIDAdmin(ModelAdmin):
    list_display = ['cart_id', 'date_added'] if hasattr(CartID, 'date_added') else ['cart_id']
    search_fields = ['cart_id']


@admin.register(CartProduct)
class CartProductAdmin(ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'is_active'] if hasattr(CartProduct, 'is_active') else ['user', 'product', 'quantity']
    list_filter = ['is_active'] if hasattr(CartProduct, 'is_active') else []
    search_fields = ['product__product_name', 'user__username']


@admin.register(UserWishList)
class UserWishListAdmin(ModelAdmin):
    list_display = ['user', 'product']
    search_fields = ['product__product_name', 'user__username']


@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ('code', 'product', 'discount_percentage', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'product__product_name')



