from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField  # PostgreSQL only

User = get_user_model()

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ("virtual", "Virtual"),
        ("in-person", "In-person"),
    ]

    name = models.CharField(max_length=255)
    category = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    description = models.TextField()
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPE_CHOICES,
        default="in-person"
    )
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    credit_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_available = models.BooleanField(default=True)
    average_rating = models.FloatField(default=0.0)
    total_sessions = models.PositiveIntegerField(default=0)
    remaining_sessions = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='services'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f"{self.name} by {self.owner.email}"
