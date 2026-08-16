from django.contrib import admin
from apps.accounts.models import UserAccount
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'role', 'is_admin', 'is_active', 'last_login', 'date_joined']
    list_editable = ['role']
    list_display_links = ['username', 'email']
    readonly_fields = ['password', 'last_login', 'date_joined']
    ordering = ['-date_joined']



admin.site.register(UserAccount, UserAccountAdmin)
