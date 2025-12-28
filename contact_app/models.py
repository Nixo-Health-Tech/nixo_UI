from django.db import models
from login_app.models import CustomUser

class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        NOT_READ = "Not_Read", "Not Read"
        READ = "Read", "Read"
        ANSWERED = "Answered", "Answered"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    full_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=TicketStatus.choices,
        default=TicketStatus.NOT_READ
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Ticket from {self.full_name} ({self.email})"