from django.db import models
from product.models import Product
from accounts.models import UserAccount


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





# user wishlist
class UserWishList(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_wishlist = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.product_name