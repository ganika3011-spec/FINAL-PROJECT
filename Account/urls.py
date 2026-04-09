from django.urls import path
from . import views

urlpatterns=[
    path("register-user",views.registerUser,name="registerUser"),
    path("register-restaurant",views.registerRestaurant,name="registerRestaurant"),
    path("login",views.login,name="login"),     
    path("logout",views.logout,name="logout"),
    path("myAccount",views.myAccount,name="myAccount"),
    path("customerdashboard",views.customerdashboard,name="customerdashboard"),
    path("restaurantdashboard",views.restaurantdashboard,name="restaurantdashboard"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]