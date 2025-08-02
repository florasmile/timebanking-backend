from django.contrib import admin
from .models import Service

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'name',
        'owner',
        'service_type',
        'credit_required',
        'is_available',
        'average_rating',
        'total_sessions',
        'remaining_sessions',
        'created_at',
    )
    
admin.site.register(Service, ServiceAdmin)