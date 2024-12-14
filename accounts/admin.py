from django.contrib import admin
from accounts.models import UserAccount
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'last_login', 'date_joined', 'is_active']
    list_display_links = ['username', 'email']
    readonly_fields = ['password', 'last_login', 'date_joined']
    ordering = ['-date_joined']


admin.site.register(UserAccount, UserAccountAdmin)
