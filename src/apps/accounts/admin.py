from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.accounts.models import UserAccount

@admin.register(UserAccount)
class UserAccountAdmin(ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_admin', 'is_active', 'last_login', 'date_joined']
    list_editable = ['role']
    list_display_links = ['username', 'email']
    readonly_fields = ['password', 'last_login', 'date_joined']
    ordering = ['-date_joined']
    list_filter = ['role', 'is_admin', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

