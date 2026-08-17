from django.db import models
from apps.product.models import Product
from apps.accounts.models import UserAccount
# Create your models here.

class PurchaseHistory(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0.0)
    payment_status = models.CharField(max_length=50, default='Completed')
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

    @property
    def total_amount(self):
        effective_price = self.price if self.price > 0 else (self.product.product_price if self.product else 0.0)
        return round(effective_price * self.quantity, 2)