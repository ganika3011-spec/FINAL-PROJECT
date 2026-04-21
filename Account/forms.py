from django import forms
from .models import User,UserProfile
from .validators import allow_only_images


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= User
        fields=["first_name","last_name","email","username","phone_number","password","confirm_password"]

    def clean(self):
        cleaned_data= super(UserForm,self).clean()
        password= cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")


class UserProfileForm(forms.ModelForm):
    address=forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"Start typing your address...","id":"id_address","required":"required"}))
    profile_picture=forms.FileField(required=False, validators=[allow_only_images], widget=forms.FileInput)
    cover_photo=forms.FileField(required=False, validators=[allow_only_images] , widget=forms.FileInput)
    # latitude=forms.CharField(required=False, widget=forms.TextInput(attrs={"readonly":"readonly"}))
    # longitude=forms.CharField(required=False, widget=forms.TextInput(attrs={"readonly":"readonly"}))
    class Meta:
        model= UserProfile
        fields=["profile_picture","cover_photo","address","country","state","city","pin_code","latitude","longitude"]
    

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            if field == "latitude" or field=="longitude":
                self.fields[field].widget.attrs["readonly"]= True

