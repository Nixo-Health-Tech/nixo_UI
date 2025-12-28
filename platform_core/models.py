from django.db import models
from django.conf import settings
from django.utils import timezone

class ToolType(models.TextChoices):
    IMAGE = "image", "Image"
    TEXT = "text", "Text"

class ToolSpec(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=16, choices=ToolType.choices, default=ToolType.IMAGE)
    is_active = models.BooleanField(default=True)
    adapter_path = models.CharField(
        max_length=255,
        help_text="مسیر کلاس آداپتر، مثل: ai_models_app.adapters.cxr.CXRAdapter"
    )
    credit_cost = models.IntegerField(default=0)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

class ExecutionStatus(models.TextChoices):
    PENDING   = "pending",   "Pending"
    RUNNING   = "running",   "Running"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED    = "failed",    "Failed"

class Execution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tool_executions")
    tool = models.ForeignKey(ToolSpec, on_delete=models.PROTECT, related_name="executions")
    input_payload = models.JSONField(default=dict, blank=True)
    output_payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=16, choices=ExecutionStatus.choices, default=ExecutionStatus.PENDING)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def duration_seconds(self):
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None
