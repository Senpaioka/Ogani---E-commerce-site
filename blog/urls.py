from django.urls import path
from blog import views


app_name = 'blog'


urlpatterns = [
    # reading blog
    path('', views.blog_page, name='blog_page'),
    path('blog_details_page/<int:blog_id>/', views.blog_details_page, name='blog_details'),
    path('category_blogs/<int:category_id>/', views.category_blog_page, name='blog_by_category'),
    # search blog
    path('blog_search/', views.blog_search_functionality, name='blog_search'),
    # blog posting, updating, editing 
    path('blog_post/', views.blog_post_page, name='blog_post'),
    path('publish_blog/', views.publish_blog_view, name='blog_publish'),
    path('update_blog/<int:blog_id>/', views.update_blog_view, name='update_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog_view, name='delete_blog'),
    # blog comment
    path('add_comment/<int:blog_id>/', views.comment_adding_view, name='add_comment'),
]
