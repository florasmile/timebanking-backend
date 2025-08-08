from django.contrib import admin
from .models import Service
from django.utils.translation import gettext_lazy as _ 
from django.forms import Textarea 
from django.contrib.postgres.fields import ArrayField 


# Custom admin filter that buckets average_rating for quick filtering
class RatingBucketFilter(admin.SimpleListFilter):
    title = _("Customer Rating")
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return (
            ("5only", "5 stars"),
            ("4_5", "4.5 & up"),
            ("4plus", "4 & up"),
            ("3_5", "3.5 & up"),
            ("3plus", "3 & up"),
            ("2_5", "2.5 & up"),
            ("2plus", "2 & up"),
            ("1plus", "1 & up"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == "5only":
            return queryset.filter(average_rating=5)
        if val == "4_5":
            return queryset.filter(average_rating__gte=4.5)
        if val == "4plus":
            return queryset.filter(average_rating__gte=4)
        if val == "3_5":
            return queryset.filter(average_rating__gte=3.5)
        if val == "3plus":
            return queryset.filter(average_rating__gte=3)
        if val == "2_5":
            return queryset.filter(average_rating__gte=2.5)
        if val == "2plus":
            return queryset.filter(average_rating__gte=2)
        if val == "1plus":
            return queryset.filter(average_rating__gte=1)
        return queryset


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'id',
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
    list_filter = (
        'service_type',
        'is_available',
        'owner',
        RatingBucketFilter,  
    )
    search_fields = (
        'name',
        'owner__email',
        'description',
    )
    date_hierarchy = 'created_at'

    # Makes ArrayField (customer_reviews) render as a big text area in admin
    formfield_overrides = {
        ArrayField: {"widget": Textarea(attrs={"rows": 4, "cols": 80})},
    }

admin.site.register(Service, ServiceAdmin)