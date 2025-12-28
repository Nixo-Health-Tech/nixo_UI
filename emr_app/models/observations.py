from django.db import models
from .core import Patient

class VitalSign(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vitals")
    datetime = models.DateTimeField()
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    systolic = models.IntegerField(null=True, blank=True)
    diastolic = models.IntegerField(null=True, blank=True)
    pulse = models.IntegerField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]

class Observation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="observations")
    datetime = models.DateTimeField()
    loinc = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=160)
    value = models.CharField(max_length=64)
    unit = models.CharField(max_length=24, blank=True)
    ref_range = models.CharField(max_length=60, blank=True)
    abnormal = models.CharField(max_length=12, blank=True)
    panel = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["-datetime"]

class DiagnosticReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reports")
    category = models.CharField(max_length=40, default="imaging")
    datetime = models.DateTimeField()
    title = models.CharField(max_length=200)
    conclusion = models.TextField(blank=True)
    text = models.TextField(blank=True)
