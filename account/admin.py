from django.contrib import admin
from .models import user_profile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_phone_number', 'user_address', 'is_verified')
    search_fields = ['user__username', 'user_phone_number', 'user_address']


admin.site.register(user_profile, UserProfileAdmin)
