from django.shortcuts import render , get_object_or_404 ,redirect
from django.contrib import messages
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from.models import Vendor
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.views import  check_vendor_user
from django.contrib.auth.decorators import user_passes_test ,login_required
from menu.forms import CategoryForm, FoodForm
from django.template.defaultfilters import slugify

# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required
@user_passes_test(check_vendor_user)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
  
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Restaurant Information Update SuccessFully!')
            return redirect('v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
            
    else: 
        profile_form = UserProfileForm(instance=profile )
        vendor_form = VendorForm(instance=vendor)
        
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/v_profile.html', context)


# Menu Builder Show Category's and button Add Category/Add Food! Show Food Etc
@login_required
@user_passes_test(check_vendor_user)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories, 
    }
    return render(request,'vendor/menu_builder.html',context)



#Food Item By Category On-click The Category 
@login_required
@user_passes_test(check_vendor_user)
def fooditem_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditem = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'category':category,
        'fooditem':fooditem,
    }
    return render(request,'vendor/fooditem_by_category.html',context)



#Category  CRUD START FROM HERE !
@login_required
@user_passes_test(check_vendor_user)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            vendor = get_vendor(request)
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,"Category Created!")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request,'vendor/add_category.html',context)



#Edit Category
@login_required
@user_passes_test(check_vendor_user)
def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            vendor = get_vendor(request)
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,"Category Updated!")
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html',context)



#DELETE CATEGORY
@login_required
@user_passes_test(check_vendor_user)
def delete_category(request,pk=None):
    get_category = get_object_or_404(Category,pk=pk)
    get_category.delete()
    messages.success(request,'Category Deleted Succesfully !')
    return redirect('menu_builder')



#FOOD ITEM CRUD Start FROM HERE!

#ADD FOOD
def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST,request.FILES)
        if form.is_valid():
            vendor = get_vendor(request)
            food_title = form.cleaned_data['food_title']
            add_food = form.save(commit=False)
            add_food.vendor = vendor
            add_food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Food Item Added Sucessfully !')
            return redirect('fooditem_by_category',add_food.category.id)
        else:
            print('form.errors')
    else:
        form = FoodForm()
    context = {
        'form':form
    }
    return render(request,'vendor/add_food.html',context)