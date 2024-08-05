from django.urls import include, path
from . import views
from accounts import views as accountviews
urlpatterns =[
    path('',accountviews.myAccount),
    path('profile/',views.v_profile,name="v_profile"),
]