from django.db import models
from vendor.models import Vendor


# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100,unique= True)
    description = models.TextField(max_length=500,blank=True)
    slug = models.SlugField(max_length=150,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        self.category_name = self.category_name.capitalize()
        
    
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural ='Categories'
    
 
    def __str__(self):
        return self.category_name
    
    
class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    food_title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500,blank=True)
    food_image = models.ImageField(upload_to='FoodImages')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    

    
    def __str__(self):
        return self.food_title