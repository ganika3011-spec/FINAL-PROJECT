from django.shortcuts import render,redirect
from django.contrib import messages 
from Account.models import UserProfile
from .forms import VendorForm
from Account.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from .models import Vendor
from django.contrib.auth.decorators import login_required,user_passes_test
from Account.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm
from django.utils.text import slugify
from django.db import IntegrityError

# Create your views here.
def get_vendor(request):
    vendor=get_object_or_404(Vendor,user=request.user)
    return vendor

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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor=get_vendor(request)
    category=Category.objects.filter(vendor=vendor)

    context={
        "category": category,
    }
    return render(request,"Vendor/menu_builder.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category, pk=pk)
    fooditems=FoodItem.objects.filter(category=category,vendor=vendor)

    context={
        "fooditems": fooditems,
        "category": category,
    }
    return render(request,"Vendor/fooditems_by_category.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    form = CategoryForm()
    if request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            slug=slugify(category_name)
            vendor=get_vendor(request)
            
            # Check if category already exists for this vendor (case-insensitive)
            if Category.objects.filter(vendor=vendor, category_name__iexact=category_name).exists():
                messages.error(request, "This category already exist")
                form.add_error('category_name', "This category already exist")
                return render(request,"Vendor/add_category.html",{"form": form})
            
            try:
                category=form.save(commit=False)
                category.vendor=vendor
                category.slug=slug
                category.save()
                messages.success(request,"Category has been added successfully!")
                return redirect('menu_builder')
            except IntegrityError:
                messages.error(request, "This category already exist")
                form.add_error('category_name', "This category already exist")
                return render(request,"Vendor/add_category.html",{"form": form})
        else:
            print(form.errors)
    context = {
        "form": form,
    }
    return render(request,"Vendor/add_category.html",context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            slug = slugify(category_name)
            vendor = get_vendor(request)
            
            # Check if category already exists for this vendor (excluding current category)
            exists = Category.objects.filter(vendor=vendor, category_name__iexact=category_name).exclude(pk=pk).exists()
            if exists:
                messages.error(request, "This category already exist")
                form.add_error('category_name', "This category already exist")
                return render(request, 'Vendor/edit_category.html', {'form': form, 'category': category})
            
            try:
                category = form.save(commit=False)
                category.vendor = vendor
                category.slug = slug
                category.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('menu_builder')
            except IntegrityError:
                messages.error(request, "This category already exist")
                form.add_error('category_name', "This category already exist")
                return render(request, 'Vendor/edit_category.html', {'form': form, 'category': category})
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'Vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')