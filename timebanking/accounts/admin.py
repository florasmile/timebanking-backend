from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Add custom fields to the detail/edit view
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "bio", "skills", "interests",
                "time_credits", "city", "state", "zip_code"
            )
        }),
    )

    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": (
                "bio", "skills", "interests",
                "time_credits", "city", "state", "zip_code"
            )
        }),
    )

    # Optional: display custom fields in the user list view
    list_display = (
        "username", "email", "city", "state", "zip_code", "time_credits", "is_staff"
    )
admin.site.register(User, CustomUserAdmin)