from django.urls import path
from review import views

app_name = 'review'


urlpatterns = [
    path('review_page/<int:product_id>', views.review_page_view, name='review_page'),
    path('review_publish/<int:product_id>/', views.review_publish_view, name='publish_review'),
]
