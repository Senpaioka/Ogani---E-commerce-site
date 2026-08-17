from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.payment.models import PurchaseHistory


@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(ModelAdmin):
    list_display = ['user', 'product', 'price', 'purchase_date'] if hasattr(PurchaseHistory, 'purchase_date') else ['id']
    search_fields = ['user__username', 'product__product_name']

