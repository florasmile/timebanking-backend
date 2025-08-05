from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import User
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

@receiver(pre_save, sender=User)
def geocode_address(sender, instance, **kwargs):
    if instance.street and instance.city and instance.state and instance.zip_code:
        address = f"{instance.street}, {instance.city}, {instance.state}, {instance.zip_code}"
        print("address", address)
        geolocator = Nominatim(user_agent="timebanking_backend")

        try:
            location = geolocator.geocode(address, timeout=10)
            print("location", location)
            if location:
                # Round to 2 decimal places, make precision within 1.1km (0.7 miles)
                instance.latitude = round(location.latitude, 2)  
                instance.longitude = round(location.longitude, 2)
                return
            # if cannot locate address provided, use zip_code instead
            elif instance.zip_code:
                print(f"Falling back to zip code geocoding for: {instance.zip_code}")
                zip_location = geolocator.geocode(
                    {"postalcode": instance.zip_code, "country": "US"},
                    timeout=10
                )
                if zip_location:
                    # Round to 2 decimal places (~1.1km precision)
                    instance.latitude = round(zip_location.latitude, 2)
                    instance.longitude = round(zip_location.longitude, 2)
                    return
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error for zip code: {e}")
            instance.latitude = None
            instance.longitude = None
    # If all attempts fail
    print("Could not geocode address - setting coordinates to None")
    instance.latitude = None
    instance.longitude = None
        