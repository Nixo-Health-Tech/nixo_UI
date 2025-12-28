from django.contrib import admin
from .models import (
    Patient, Practitioner, Location, Encounter,
    Condition, AllergyIntolerance, Medication, MedicationStatement, Immunization,
    VitalSign, Observation, DiagnosticReport,
    DocumentReference
)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "dob", "sex", "owner")
    search_fields = ("full_name", "email")

admin.site.register([Practitioner, Location, Encounter])
admin.site.register([Condition, AllergyIntolerance, Medication, MedicationStatement, Immunization])
admin.site.register([VitalSign, Observation, DiagnosticReport])
admin.site.register([DocumentReference])
