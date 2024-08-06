from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator
class VendorForm(forms.ModelForm): #This must be FileField If ImageField Validator.py will not Work
    vendor_license=forms.FileField (widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator]) #This Way we Can Actually Use Custom CSS Class
    class Meta:
        model = Vendor 
        fields = ['vendor_name','vendor_license']