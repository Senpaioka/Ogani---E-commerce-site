from django.db import models
from apps.accounts.models import UserAccount
from apps.product.models import Product
# Create your models here.

class ProductReview(models.Model):

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star = models.IntegerField(default=0)
    review = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username