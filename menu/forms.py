from accounts.validators import allow_only_images_validator
from .models import Category ,FoodItem
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
        
        
class FoodForm(forms.ModelForm):
    food_image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator]) #This Way we Can Actually Use Custom CSS Class
    class Meta:
        model = FoodItem
        fields = ['food_title','category','food_image','description','price','is_available']