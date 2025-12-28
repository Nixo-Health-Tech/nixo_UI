from django.contrib import admin
from .models import BreastCancerRiskAssessment

@admin.register(BreastCancerRiskAssessment)
class BreastAssessmentAdmin(admin.ModelAdmin):
    list_display = ("id","age","gender","ethnicity","created_at")
    list_filter = ("gender","ethnicity","created_at")
    search_fields = ("id",)
