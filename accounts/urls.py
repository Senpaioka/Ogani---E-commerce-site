from django.urls import path
from accounts import views


app_name = 'account'

urlpatterns = [
    path('registration/', views.registration_page, name='registration_page'),
    path('login/', views.login_page, name='login_page'),
]
