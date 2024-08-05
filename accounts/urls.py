from django.urls import include, path
from . import views
urlpatterns =[
    # registerUser and Vendor
    path('',views.myAccount),
    path('registerUser/',views.registeruser,name="registeruser"),
    path('registerVendor/',views.registerVendor,name="registerVendor"),
    
    #LogIn and LogOut
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    
    #User and vendor Active My Email Verification!
    path('myAccount/',views.myAccount,name="myAccount"),
    path('custDashboard/',views.custDashboard,name="custDashboard"),
    path('vendorDashboard/',views.vendorDashboard,name="vendorDashboard"),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    
    #Forget password Rest 
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>',views.reset_password_validate,name="reset_password_validate"),
    path('reset_password/',views.reset_password,name="reset_password"),
    
    #Vendor DashBoard
    path('vendor/',include("vendor.urls")),
]