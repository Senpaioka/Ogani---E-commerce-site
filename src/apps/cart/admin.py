from django.contrib import admin
from apps.cart.models import CartID, CartProduct, UserWishList, Coupon

# Register your models here.
admin.site.register(CartID)
admin.site.register(CartProduct)
admin.site.register(UserWishList)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'product', 'discount_percentage', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'product__product_name')


