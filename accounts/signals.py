from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import User
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# helper to set and round coordinates
def set_coordinates(instance, latitude, longitude):
    # Round to 2 decimal places, make precision within 1.1km (0.7 miles)
    instance.latitude = round(latitude, 2)
    instance.longitude = round(longitude, 2)

# try geocode with error handling
def try_geocode(geolocator, query, timeout=10):
    try:
        return geolocator.geocode(query, timeout=timeout)
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return None
    
@receiver(pre_save, sender=User)
def geocode_address(sender, instance, **kwargs):

    geolocator = Nominatim(user_agent="timebanking_backend")
    location = None

    # try full address first
    if instance.street and instance.city and instance.state and instance.zip_code:
        address = f"{instance.street}, {instance.city}, {instance.state}, {instance.zip_code}"
        location = try_geocode(geolocator, address)
        # if cannot locate address provided, use zip_code instead
    if not location and instance.zip_code:
            location = geolocator.geocode(
                {"postalcode": instance.zip_code, "country": "US"}
            )
    if location:
        set_coordinates(instance, location.latitude, location.longitude)
    else:
        print("Could not geocode address - setting coordinates to None")
        set_coordinates(instance, None, None)