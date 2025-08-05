from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import User

@receiver(pre_save, sender=User)
def geocode_address(sender, instance, **kwargs):
    if instance.street and instance.city and instance.state and instance.zip_code:
        address = f"{instance.street}, {instance.city}, {instance.state}, {instance.zip_code}"
        geolocator = Nominatim(user_agent="timebanking_backend")

        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                # Round to 2 decimal places, make precision within 1.1km (0.7 miles)
                instance.latitude = round(location.latitude, 2)  
                instance.longitude = round(location.longitude, 2)
        except Exception as e:
            instance.latitude = None
            instance.longitude = None