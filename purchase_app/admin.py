from django.contrib import admin
from .models import Product, Price, Subscription, Order, Wallet, UsageLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","slug","type","active")
    list_filter = ("type","active")
    search_fields = ("name","slug")

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("product","kind","unit_amount","currency","active","interval","interval_count","credits_included")
    list_filter = ("kind","currency","active")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user","price","status","current_period_end","cancel_at_period_end")
    list_filter = ("status",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user","price","total_amount","currency","status","provider","created_at","paid_at")
    list_filter = ("status","currency","provider")

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user","credits")

@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ("user","product","credits_spent","created_at")
    list_filter = ("product",)
