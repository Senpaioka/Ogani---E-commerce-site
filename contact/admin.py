from django.contrib import admin
from contact.models import ContactInfoModel, ContactFormModel, NewsLetterModel

# Register your models here.

class ContactInfoAdmin(admin.ModelAdmin):

    list_display = ['address', 'created_at']    
    ordering = ['-created_at']

admin.site.register(ContactInfoModel, ContactInfoAdmin)




class ContactFormAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'email', 'sending_time']
    list_display_links = ['name', 'email']
    readonly_fields = ['sending_time']
    ordering = ['-sending_time']

admin.site.register(ContactFormModel, ContactFormAdmin)







class NewsLetterAdmin(admin.ModelAdmin):

    list_display = ['email', 'send_time']
    ordering = ['-send_time']

admin.site.register(NewsLetterModel, NewsLetterAdmin)