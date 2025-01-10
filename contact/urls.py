from django.urls import path
from contact import views


app_name = 'contact'

urlpatterns = [
    path('contact_page/', views.contact_page_view, name='contact_page'),
    path('send_message/', views.contact_message_save, name='save_message'),
    path('subscribe/', views.subscribe_user_from_newsletter, name='newsletter_subscribe'),
]
