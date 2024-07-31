from django.shortcuts import render , HttpResponse , redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.

def registeruser(request):
    if request.method == "POST":
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
            messages.success(request," User Account Register Sucessfully ")
            
            return redirect('registeruser')
        else:
            print("Invalid Form")
            print(form.errors)
            
    else:
            
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)