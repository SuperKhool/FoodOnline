from django.shortcuts import render , HttpResponse , redirect

from vendor.forms import VendorForm
from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages , auth
from .utils import DetectUser, send_verification_email ,check_valid_user
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



# Create your views here.



#Restrict Vendor User To Access Customer Dashboard
def check_vendor_user(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


#Restrict Customer  User To Access Vendor Dashboard
def check_customer_user(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    



def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are All ready Logged In!')
        return redirect('myAccount')
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # This Way We can save Or say HASH password
            
            # password = form.cleaned_data['password']
            # user=form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            
            #Create The User by .models Creat_User class
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name,last_name = last_name, username = username, email = email,password = password)
            user.role = User.CUSTOMER
            user.save()
            #Send Verification Email
            mail_subject = "Please Active  Your Account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, mail_subject , email_template)
            messages.success(request," User Account Register Sucessfully! Check Email For Activation!")
            
            
            return redirect('login')
        else:
            print("Invalid Form")
            print(form.errors)
            
    else:
            
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)




def registerVendor(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username =username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)            
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            #Send Verification Email
            mail_subject = "Please Active  Your Account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request,user, mail_subject , email_template)
            messages.success(request,"Your Account Register Successfully! Please Wait for The Approval! ")
            return redirect('registerVendor')
        else:
            print("invalid form")
            print(form.errors)
    else:
         form = UserForm()
         v_form = VendorForm()
               
    context = {
        'form': form,
        'v_form': v_form,
    }   
    return render(request,'accounts/registerVendor.html',context)




#Active The User By is_active status set to  True
def activate(request ,uidb64,token):
     
    # user = check_valid_user(request.user,uidb64) #{I made A Helper Fucntion For It : Utils }
    try:
        uid =urlsafe_base64_decode(uidb64).decode() #Decodeing The User Primery Key! COMES FROM django.utils.http
        user = User._default_manager.get(pk=uid) #after Decoding PK Getting USER From The User Model 
    except(TypeError,ValueError,OverflowError,User.DoesNotExist): #Checking If User Doseno't Exist What Happen!
        user = None
        
        
    if user is not None and default_token_generator.check_token(user,token): #Checking USER AND Also The TOken By Token Genaretor Cmoes form django.contrib.Auth.token
        if user.role == 1:  
            user.is_active = True
            user.save()
            messages.success(request,'Congratulation! Your Restaurant Status is Active! Please Wait For The Aproval!')
            return redirect('myAccount')
        elif user.role == 2:
            user.is_active = True
            user.save()
            messages.success(request,'Congratulation! User Active Sucessfull.')
            return redirect('myAccount')
    else: 
        messages.error(request,'User Validation Failed .')
        return redirect('myAccount')
    
        





def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are All ready Logged In!')
        return redirect('dashboard')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Logged In Sucessfully! ")
            return redirect('myAccount')
        else:
            messages.error(request,"Something Gose Wrong! ")
            return redirect('login')

    return render(request,'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request,'Logged Out Sucessfully!')
    return  redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = DetectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_customer_user) # user Passes Test Deafult Decoretor Help To veryfi user role if it's pass user can acess the Dashboard 
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_vendor_user)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')




def forgot_password(request):
    
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact = email)
            
            mail_subject = "Reset Your Password"
            email_template ='accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"Password Reset email Has Send To Your email address")
            return redirect('login')
        else:
            messages.success(request,"Email Dose Not Exist")
            return redirect('forgot_password')  
    
    return render(request,'accounts/forgot_password.html')


def reset_password_validate(request,uidb64,token):
    user , uid =check_valid_user(request.user,uidb64)
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid #Saving The User id to the request session So that We can get it This User_id on the Reset_Password.html  
        messages.info(request,"Please Reset Your Passwrod")
        return redirect('reset_password')
    else:
        messages.warning(request , 'This Link Has Expierd ')
        return redirect('myAccount')
    
     


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')#Now Getting The User_id From The reset_password_validate.html or Function in views
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request ," Password Reset Sucessfully!")
            return redirect('login')
        else:
            messages.warning(request,'Password Dose Not Matched')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')