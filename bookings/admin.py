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
    list_filter = (
        'status',
        'service__service_type',
        'customer',
        'owner',
    )
    search_fields = (
        'service__name',
        'customer__email',
        'owner__email',
    )
    date_hierarchy = 'booked_at'

admin.site.register(Booking, BookingAdmin)