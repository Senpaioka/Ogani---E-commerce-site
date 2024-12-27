from django.urls import path
from home import views


app_name = 'home'


urlpatterns = [
    path('', views.home_view, name='home_page'),
    path('search_product/', views.product_search_view, name='search_product'),
]


