from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.review.models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ['user', 'product', 'star', 'review', 'created_at']
    list_filter = ['star', 'created_at']
    search_fields = ['user__username', 'product__product_name', 'review']
