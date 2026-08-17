from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.contact.models import ContactInfoModel, ContactFormModel, NewsLetterModel


@admin.register(ContactInfoModel)
class ContactInfoAdmin(ModelAdmin):
    list_display = ['address', 'created_at']    
    ordering = ['-created_at']


@admin.register(ContactFormModel)
class ContactFormAdmin(ModelAdmin):
    list_display = ['name', 'email', 'sending_time']
    list_display_links = ['name', 'email']
    readonly_fields = ['sending_time']
    search_fields = ['name', 'email', 'message']
    ordering = ['-sending_time']


@admin.register(NewsLetterModel)
class NewsLetterAdmin(ModelAdmin):
    list_display = ['email', 'send_time']
    search_fields = ['email']
    ordering = ['-send_time']