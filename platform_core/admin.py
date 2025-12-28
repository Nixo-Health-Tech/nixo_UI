from django.contrib import admin
from .models import ToolSpec, Execution

@admin.register(ToolSpec)
class ToolSpecAdmin(admin.ModelAdmin):
    list_display = ("name","slug","type","is_active","credit_cost")
    list_filter = ("type","is_active")
    search_fields = ("name","slug")

@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = ("id","tool","user","status","started_at","finished_at")
    list_filter = ("status","tool")
    search_fields = ("id","tool__name","user__phone_number","user__email")
