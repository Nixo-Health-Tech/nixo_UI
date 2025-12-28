from django.db import models
from .core import Patient

class DocumentReference(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=40, default="document")
    file = models.FileField(upload_to="emr/docs/")
    mime = models.CharField(max_length=100, blank=True)
    size_bytes = models.BigIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text_cache = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
