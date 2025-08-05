from django.contrib import admin
from .models import Booking

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'id',
        'status',
        'booked_at',
        'completed_at',
        'customer_review',
        'customer_rating',
        'owner_id',
        'customer_id',
        'service_id',
    )
    
admin.site.register(Booking, BookingAdmin)