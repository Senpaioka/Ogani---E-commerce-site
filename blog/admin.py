from django.contrib import admin
from blog.models import BlogCategory, BlogModel

# Register your models here.

admin.site.register(BlogCategory)
admin.site.register(BlogModel)

