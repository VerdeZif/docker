from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_admin", "is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

admin.site.register(User, UserAdmin)
