from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    mode=CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Profile Info", {"fields":("profile_pic",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile Info", {"fields":("profile_pic",)}),
    )

admin.site.register(CustomUser,CustomUserAdmin)