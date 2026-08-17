from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from apps.product.models import Product, ProductCategory, ProductGallery
from django.utils.html import format_html


class ProductGalleryAdmin(StackedInline):
    model = ProductGallery
    extra = 0


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['product_name', 'product_category', 'product_price', 'is_available']
    list_editable = ['is_available']
    list_filter = ['product_category', 'is_available']
    search_fields = ['product_name', 'product_description']
    inlines = [ProductGalleryAdmin]


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ["image_tag", "product_category"]
    search_fields = ["product_category"]

    def image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px; border-radius:6px; object-fit:cover;"/>', obj.category_image.url)
        return 'No Image Available'



