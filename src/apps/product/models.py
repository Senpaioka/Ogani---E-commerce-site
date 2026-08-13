from django.db import models

# Create your models here.


class ProductCategory(models.Model):

    PRODUCT_CATEGORY_CHOICES = [
        ('meats', 'meats'),
        ('fruits', 'fruits'),
        ('vegetables', 'vegetables'),
        ('drinks', 'drinks'),
        ('others', 'others'),
    ]

    product_category = models.CharField(max_length=10, choices=PRODUCT_CATEGORY_CHOICES)
    category_image = models.ImageField(upload_to='category/photos', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name_plural = "Product Categories"

    def __str__(self):
        return self.product_category











class Product(models.Model):

    product_name = models.CharField(max_length=100)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    product_info = models.CharField(max_length=255, blank=True)
    product_description = models.TextField(blank=True)
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to='product/photos')
    product_weight = models.FloatField()
    shipping = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_name
    




class ProductGallery(models.Model):
    class Meta:
        verbose_name = "Product Thumbnail"
        verbose_name_plural = "Product Thumbnails"

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Product')
    gallery = models.ImageField(upload_to ='product/thumbnails', null=True, blank=True)
    












