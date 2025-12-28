# --- Additions for tool registry & runs ---
from django.db import models
from django.conf import settings

class ToolType(models.TextChoices):
    IMAGE = "image", "Image"
    TEXT = "text", "Text"

class AIModelTool(models.Model):
    """Registry of AI tools (e.g., CXR, Breast CA screening, etc.)."""
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)  # e.g. 'cxr', 'breast_cancer'
    type = models.CharField(max_length=16, choices=ToolType.choices, default=ToolType.IMAGE)
    active = models.BooleanField(default=True)
    credit_cost = models.IntegerField(default=0)   # per-use credits (for purchase_app)
    meta = models.JSONField(default=dict, blank=True)  # any config

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class RunStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    DONE = "done", "Done"
    ERROR = "error", "Error"

class ModelRun(models.Model):
    """Generic run entry. Input (file/text), result JSON, optional overlay image."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_model_runs")
    tool = models.ForeignKey(AIModelTool, on_delete=models.PROTECT, related_name="runs")
    # optional link to EMR patient
    from emr_app.models import Patient  # import here to avoid circular import at top
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="ai_model_runs")
    # inputs (for image tools we use image; for text tools, use prompt field)
    image = models.ImageField(upload_to="ai/models/inputs/", null=True, blank=True)
    prompt = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=RunStatus.choices, default=RunStatus.PENDING)
    result = models.JSONField(default=dict, blank=True)
    overlay_image = models.ImageField(upload_to="ai/models/overlays/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    credits_charged = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
