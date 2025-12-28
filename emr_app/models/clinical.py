from django.db import models
from .core import Patient

class Condition(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="conditions")
    onset = models.DateField(null=True, blank=True)
    code = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=40, default="active")  # active|inactive|resolved
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["description"]

class AllergyIntolerance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="allergies")
    substance = models.CharField(max_length=120)
    reaction = models.CharField(max_length=255, blank=True)
    severity = models.CharField(max_length=20, blank=True)  # mild|moderate|severe
    status = models.CharField(max_length=20, default="active")

class Medication(models.Model):
    rxnorm = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=200)
    form = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.name

class MedicationStatement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medications")
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    dose = models.CharField(max_length=80, blank=True)
    route = models.CharField(max_length=40, blank=True)
    frequency = models.CharField(max_length=80, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")
    notes = models.TextField(blank=True)

class Immunization(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="immunizations")
    vaccine = models.CharField(max_length=120)
    date = models.DateField()
    lot_number = models.CharField(max_length=80, blank=True)
    site = models.CharField(max_length=60, blank=True)
