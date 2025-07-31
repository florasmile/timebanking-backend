from django.db import models
# Create your models here.

class Service:
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True) 
    time_credits = models.DecimalField(max_digits=6, decimal_places=1, default=0) # default unit: hour
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)

    def __str__(self):
        return self.username