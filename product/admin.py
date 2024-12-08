from django.contrib import admin
from product.models import Product, ProductCategory, ProductGallery
from django.utils.html import format_html

# Register your models here.


class ProductGalleryAdmin(admin.StackedInline):
    model = ProductGallery
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_category', 'product_price', 'is_available']
    list_editable = ['is_available']
    inlines = [ProductGalleryAdmin]

admin.site.register(Product, ProductAdmin)





class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = ["image_tag", "product_category"]

    # displaying images
    def image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.category_image.url))
        else:
            return 'No Image Available'


admin.site.register(ProductCategory, ProductCategoryAdmin)


