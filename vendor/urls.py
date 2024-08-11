from django.urls import include, path
from . import views
from accounts import views as accountviews
urlpatterns =[
    path('',accountviews.myAccount),
    path('profile/',views.v_profile,name="v_profile"),
    path('menu-builder/',views.menu_builder,name="menu_builder"),
    path('menu-builder/category/<int:pk>/',views.fooditem_by_category,name="fooditem_by_category"),
    
    #CATEGORY CRUD
    path('menu-builder/category/add/',views.add_category,name="add_category"),
    path('menu-builder/category/edit/<int:pk>/',views.edit_category,name="edit_category"),
    path('menu-builder/delete/<int:pk>/',views.delete_category,name="delete_category"),
    
    #FOODITEM CRUD
    path('menu-builder/food/add/',views.add_food,name="add_food"),
]