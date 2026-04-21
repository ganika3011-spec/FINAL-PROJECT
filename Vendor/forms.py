from django import forms
from .models import Vendor
from Account.validators import allow_only_images

class VendorForm(forms.ModelForm):
    vendor_license=forms.FileField(required=False, validators=[allow_only_images], widget=forms.FileInput)
    class Meta:
        model= Vendor
        fields=["vendor_name","vendor_license"]

