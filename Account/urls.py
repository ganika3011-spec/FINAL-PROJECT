from django.urls import path
from . import views

urlpatterns=[
    path("register-user",views.registerUser,name="registerUser"),
    path("register-restaurant",views.registerRestaurant,name="registerRestaurant"),
]