from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from Vendor.forms import VendorForm

# Create your views here.
def registerUser(request):
    if request.method=='POST':
        print(request.POST)
        form= UserForm(request.POST)
        if form.is_valid():
            # create the user usingthe form data
            # password=form.cleaned_data['password']
            # user=form.save(commit=False)
            # user.role=User.CUSTOMER # here we add the extra filled after the form is saved.
            # user.set_password(password)  # Set the password using Django's set_password method
            # user.save()

            # Create the user by creste_user method of MyAccountManager class.
            first_name= form.cleaned_data["first_name"]
            last_name= form.cleaned_data["last_name"]
            email= form.cleaned_data["email"]
            username= form.cleaned_data["username"]
            
            password= form.cleaned_data["password"]

            user=User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                
                password=password,
            )
            user.Role='Customer'
            user.save()
            messages.success(request,"Your account has been registered successfully!")
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form= UserForm()
    context={
        'form':form,
    }
    return render(request, 'accounts/register-user.html',context)

def registerRestaurant(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name= form.cleaned_data["first_name"]
            last_name= form.cleaned_data["last_name"]
            email= form.cleaned_data["email"]
            username= form.cleaned_data["username"]
            
            password= form.cleaned_data["password"]

            user=User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                
                password=password,
            )
            user.Role='Vendor'
            user.save()

            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile= UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()

            messages.success(request,"Your account has been registered successfully! please wait for the admin approval.")
            return redirect('registerRestaurant')
        else:
            print(form.errors)
            print(v_form.errors)
    else:
        form= UserForm()
        v_form= VendorForm()
    context={
        'form':form,
        'v_form':v_form,
    }
    return render(request, 'accounts/register-restaurant.html',context)
