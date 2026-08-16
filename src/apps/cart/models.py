from django.db import models
from apps.product.models import Product
from apps.accounts.models import UserAccount


# Create your models here.

# saving user session id
class CartID(models.Model):
    cart_id = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    




# product details in cart
class  CartProduct(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    user_session = models.ForeignKey(CartID, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

    def sub_total(self):
        return self.quantity * self.price

    @property
    def raw_subtotal(self):
        if hasattr(self, '_raw_subtotal'):
            return self._raw_subtotal
        if self.product and hasattr(self.product, 'product_price'):
            return round(self.product.product_price * self.quantity, 2)
        return round(self.price * self.quantity, 2)

    @raw_subtotal.setter
    def raw_subtotal(self, value):
        self._raw_subtotal = value

    @property
    def discounted_subtotal(self):
        if hasattr(self, '_discounted_subtotal'):
            return self._discounted_subtotal
        return self.raw_subtotal

    @discounted_subtotal.setter
    def discounted_subtotal(self, value):
        self._discounted_subtotal = value

    @property
    def discount_amount(self):
        return getattr(self, '_discount_amount', 0)

    @discount_amount.setter
    def discount_amount(self, value):
        self._discount_amount = value

    @property
    def has_coupon(self):
        return getattr(self, '_has_coupon', False)

    @has_coupon.setter
    def has_coupon(self, value):
        self._has_coupon = value






# user wishlist
class UserWishList(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_wishlist = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.product_name


# product coupon
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="Coupon code, e.g. SAVE25")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='coupons', null=True, blank=True, help_text="Product this coupon applies to (leave empty for storewide discount)")
    discount_percentage = models.PositiveIntegerField(default=25, help_text="Percentage discount, e.g. 25 for 25%")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"{self.code} ({self.discount_percentage}% off {self.product.product_name})"
        return f"{self.code} ({self.discount_percentage}% off entire cart)"
