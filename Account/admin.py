from django.contrib import admin
from .models import User,UserProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields=('password',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'Role', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('Role', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user' , 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude')
    search_fields = ('user__email', 'user__username')
    list_filter = ('country', 'state', 'city')
    ordering = ('-created_at',)