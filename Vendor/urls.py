from django.urls import path
from . import views 
from Account import views as account_views

urlpatterns = [
    path("", account_views.restaurantdashboard, name='vendor'),
    path("profile/", views.vendorProfile, name="vendorProfile"),
]