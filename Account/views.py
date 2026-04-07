from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login as auth_login
from Vendor.forms import VendorForm
from .utils import detect_user_role
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied



# Restrict the vendor from accessing the customer dashboard and vice versa. 
def check_role_vendor(user):
    if user.Role == User.RESTAURANT:
        return True
    else:
        raise PermissionDenied
    

def check_role_customer(user):
    if user.Role == User.CUSTOMER:
        return True
    else:
        raise PermissionDenied






def registerUser(request):
    if request.user.is_authenticated:
            messages.info(request,"You are already logged in!")
            return redirect('dashboard')
    elif request.method=='POST':
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
    if request.user.is_authenticated:
            messages.info(request,"You are already logged in!")
            return redirect('dashboard')
    elif request.method=='POST':
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
            user.Role='Restaurant'
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

def login(request):
        if request.user.is_authenticated:
            messages.info(request,"You are already logged in!")
            return redirect('myAccount')
        elif request.method=='POST':
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
            if user is not None:
                auth_login(request,user)
                messages.success(request,"You are logged in!")
                return redirect('myAccount')
            else:
                messages.error(request,"Invalid login credentials!")
                return redirect('login')
        
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out!")
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirect_url= detect_user_role(user)
    return redirect(redirect_url)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerdashboard(request):     
    return render(request, 'accounts/customerdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def restaurantdashboard(request):
    return render(request, 'accounts/restaurantdashboard.html')

