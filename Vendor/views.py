from django.shortcuts import render,redirect
from django.contrib import messages 
from Account.models import UserProfile
from .forms import VendorForm
from Account.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from .models import Vendor
from django.contrib.auth.decorators import login_required,user_passes_test
from Account.views import check_role_vendor


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    profile=get_object_or_404(UserProfile, user=request.user)
    vendor=get_object_or_404(Vendor, user=request.user)

    if request.method=="POST":
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"Your profile has been updated successfully!")
            return redirect('vendorProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:   
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {

        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "vendor": vendor,
        "profile": profile,
    }
    return render(request, "Vendor/vendorProfile.html",context)