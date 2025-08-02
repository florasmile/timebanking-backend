from django.db import models
from django.conf import settings
from services.models import Service

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    customer_review = models.TextField(blank=True)
    customer_rating = models.IntegerField(null=True, blank=True)

  #retain booking records when the owner/customer/service is deleted
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='owned_bookings'
      )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customer_bookings'
      )
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
      )

    def __str__(self):
        return f"Booking #{self.id} - {self.status}"