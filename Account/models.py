from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager




class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user= self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,    
        )
        user.is_active=True
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True

        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    RESTAURANT = 'Restaurant'
    CUSTOMER = 'Customer'
    ADMIN = 'Admin'

    ROLE_CHOICES=(
    (CUSTOMER, 'Customer'),
    (RESTAURANT, 'Restaurant'),
    (ADMIN, 'Admin'), 
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)
    Role= models.CharField(max_length=50,choices=ROLE_CHOICES,default=CUSTOMER)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']

    objects=MyAccountManager() #to access the methods of MyAccountManager class through User.

    
    #required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
    
    def get_role(self):
        if self.Role=='Customer':
            return 'Customer'
        elif self.Role=='Restaurant':
            return 'Restaurant'
        elif self.Role=='Admin':
            return 'Admin'
        else:            return 'No Role Assigned'

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    profile_picture=models.ImageField(upload_to='users/profile_pictures',null=True,blank=True)
    cover_photo=models.ImageField(upload_to='users/cover_photos',null=True,blank=True)
    address=models.CharField(max_length=250,null=True,blank=True)    
    
    city=models.CharField(max_length=20,null=True,blank=True)
    state=models.CharField(max_length=20,null=True,blank=True)
    country=models.CharField(max_length=20,null=True,blank=True)
    pin_code=models.CharField(max_length=10,null=True,blank=True)
    latitude=models.CharField(null=True,blank=True)
    longitude=models.CharField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    # def full_address(self):
    #     return f'{self.address_line_1} {self.address_line_2}'
    
