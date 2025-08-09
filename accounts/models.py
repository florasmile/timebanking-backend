from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.contrib.postgres.fields import ArrayField 
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None  # disable username field
    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)  # Add default
    
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    interests = ArrayField(models.CharField(max_length=50), blank=True, default=list) 
    time_credits = models.DecimalField(max_digits=4, decimal_places=1, default=3.0) # default unit: hour
    street = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    state = models.CharField(max_length=100, blank=False)
    zip_code = models.CharField(max_length=10, blank=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    avatar = CloudinaryField('avatar', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email