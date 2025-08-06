from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class CustomUserAdmin(UserAdmin):
    # Add custom fields to the detail/edit view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "bio", "skills", "interests")
        }),
        ("Location Info", {
            "fields": ("street", "city", "state", "zip_code")
        }),
        ("Credits", {
            "fields": ("time_credits",)
        }),
        ("Avatar", {
            "fields": ("avatar",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    # Fields to show when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name"),
        }),
        ("Additional Info", {
            "fields": ("bio", "skills", "interests", "time_credits", "street", "city", "state", "zip_code", "avatar"),
        }),
    )

    list_display = ("id","email", "is_verified", "first_name", "last_name", "street", "city", "state", "zip_code", "time_credits", "is_staff")
    search_fields = ("email", "first_name", "last_name", "city", "state", "zip_code")
    ordering = ("id",)

admin.site.register(User, CustomUserAdmin)