from django.contrib import admin
from blog.models import BlogCategory, BlogModel, BlogCommentModel, BlogCommentTracker

# Register your models here.

admin.site.register(BlogCategory)
admin.site.register(BlogModel)
admin.site.register(BlogCommentModel)
admin.site.register(BlogCommentTracker)

