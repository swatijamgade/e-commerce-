from django.contrib import admin
from .models import Profile, Address

# Register your models here.


# admin.site.register(Profile)
# admin.site.register(Address)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile']
    search_fields = ['user', 'mobile']
    list_filter = ['user', 'mobile']
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['profile', 'type', 'city', 'country', 'pin_code']
    search_fields = ['profile', 'type', 'city', 'country', 'pin_code']
    list_filter = ['profile', 'type', 'city', 'country', 'pin_code']
    list_per_page = 10