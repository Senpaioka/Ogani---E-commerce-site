from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.blog.models import BlogCategory, BlogModel, BlogCommentModel, BlogCommentTracker


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ['category', 'created_at']
    search_fields = ['category']


@admin.register(BlogModel)
class BlogModelAdmin(ModelAdmin):
    list_display = ['title', 'blog_category', 'author', 'created_at']
    search_fields = ['title', 'blog_body']
    list_filter = ['blog_category', 'created_at']


@admin.register(BlogCommentModel)
class BlogCommentModelAdmin(ModelAdmin):
    list_display = ['id', 'user', 'blog', 'created_at']
    search_fields = ['comment', 'user__username', 'blog__title']


@admin.register(BlogCommentTracker)
class BlogCommentTrackerAdmin(ModelAdmin):
    list_display = ['id', 'blog', 'comment_count']



