from django.db import models
from django.conf import settings

class ProductType(models.TextChoices):
    CREDITS = "credits", "Credit Pack"
    PER_USE = "per_use", "Per-Use Service"
    SUBSCRIPTION = "subscription", "Subscription"

class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=20, choices=ProductType.choices)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self): return self.name

class PriceKind(models.TextChoices):
    ONE_TIME = "one_time", "One-time"
    RECURRING = "recurring", "Recurring"

class Price(models.Model):
    product = models.ForeignKey(Product, related_name="prices", on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=PriceKind.choices)
    currency = models.CharField(max_length=10, default="EUR")
    unit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=10, blank=True)  # e.g., 'month'
    interval_count = models.IntegerField(default=1)
    trial_days = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    credits_included = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} | {self.kind} {self.unit_amount} {self.currency}"

class SubscriptionStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CANCELED = "canceled", "Canceled"
    PAST_DUE = "past_due", "Past Due"

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    price = models.ForeignKey(Price, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    price = models.ForeignKey(Price, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="EUR")
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    provider = models.CharField(max_length=50, default="manual")
    provider_ref = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    credits = models.IntegerField(default=0)

class UsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usage_logs")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    credits_spent = models.IntegerField(default=0)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
