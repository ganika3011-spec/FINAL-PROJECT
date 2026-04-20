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
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from Vendor.models import Vendor
from django.contrib.auth.tokens import default_token_generator




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
            return redirect('myAccount')
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
            user.Role=User.CUSTOMER
            user.save()
            
            mail_subject = 'Please, Activate your account.'
            email_template = 'accounts/emails/acc_active_email.html'
            send_verification_email(request,user,mail_subject,email_template)
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
            user.Role=User.RESTAURANT
            user.save()

            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile= UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            
            mail_subject = 'Please, Activate your account.'
            email_template = 'accounts/emails/acc_active_email.html'
            send_verification_email(request,user,mail_subject,email_template)
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

def activate(request, uidb64, token):
    """Activate user account via email verification link"""
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('myAccount')

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


def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request,"Account does not exist with this email address.")
            return redirect('forgot_password')
    return render(request,"accounts/forgot_password.html")

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request,"Please reset your password.")
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired.')
        return redirect('myAccount')

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            uid=request.session.get('uid')
            user=User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successful! Please login with your new password.")
            return redirect('login')
        else:
            messages.error(request,"Password do not match!")
            return redirect('reset_password')
    return render(request,"accounts/reset_password.html")