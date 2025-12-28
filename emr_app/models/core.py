from django.db import models
from django.conf import settings

class Patient(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=64, blank=True)
    full_name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

class Practitioner(models.Model):
    name = models.CharField(max_length=150)
    specialty = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Encounter(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="encounters")
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    practitioner = models.ForeignKey(Practitioner, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["-start"]
