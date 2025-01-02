from django.urls import path
from blog import views


app_name = 'blog'


urlpatterns = [
    path('', views.blog_page, name='blog_page'),
    path('blog_details_page/<int:blog_id>/', views.blog_details_page, name='blog_details'),
    path('category_blogs/<int:category_id>/', views.category_blog_page, name='blog_by_category'),
    path('blog_search/', views.blog_search_functionality, name='blog_search'),
    path('blog_post/', views.blog_post_page, name='blog_post'),
    path('publish_blog/', views.publish_blog_view, name='blog_publish'),
]
