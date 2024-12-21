from django.contrib import admin
from cart.models import CartID, CartProduct, UserWishList

# Register your models here.
admin.site.register(CartID)
admin.site.register(CartProduct)
admin.site.register(UserWishList)

