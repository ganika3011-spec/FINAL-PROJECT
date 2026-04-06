from django.contrib import admin
from .models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ("user",'vendor_name', 'is_approved','created_at')
    search_fields = ('vendor_name', 'vendor_license', 'user__username')
    list_display_links = ('user', 'vendor_name')
    list_filter = ('is_approved', 'created_at')
admin.site.register(Vendor,VendorAdmin)
