from django.contrib import admin

# Register your models here.
from .models import Category,FoodItem

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','vendor','updated_at',)
    search_fields = ('category_name','vendor__vendor_name',)


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title','category','vendor','updated_at','is_available',)
    search_fields= ('food_title','category__category_name','vendor__vendor_name')
    list_filter = ('is_available',)

admin.site.register(Category ,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)