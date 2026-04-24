from django.urls import path
from . import views 
from Account import views as account_views

urlpatterns = [
    path("", account_views.restaurantdashboard, name='vendor'),
    path("profile/", views.vendorProfile, name="vendorProfile"),
    path("menu/", views.menu_builder, name="menu_builder"),
    path("menu/category/<int:pk>/", views.fooditems_by_category, name="fooditems_by_category"),
    path("menu/category/add/", views.add_category, name="add_category"),
    path("menu/category/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path("menu/category/delete/<int:pk>/", views.delete_category, name="delete_category"),
    # path("menu/food/add/", views.add_food, name="add_food"),
    # path("menu/food/edit/<int:pk>/", views.edit_food, name="edit_food"),
    # path("menu/food/delete/<int:pk>/", views.delete_food, name="delete_food"),  
]