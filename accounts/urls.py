from django.urls import path
from accounts import views


app_name = 'account'

urlpatterns = [
    path('registration/', views.registration_page, name='registration_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile_page, name='profile_page'),
    path('update/', views.user_update_page, name='update_page'),
    path('settings/', views.user_settings_page, name='settings_page'),
]
