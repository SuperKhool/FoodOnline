from django.core.exceptions import ValidationError
import os 

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] # i need the extension only right so i index 1 ...so tha image.jpg  this image is 0 index and .jpg is 1
    print(ext)
    valid_ext = ['.png','.jpg','.img','.jpeg']
    if not ext.lower() in valid_ext:
        raise ValidationError("Unsupported extension. Please upload a valid file with one of the following extensions: " +str(valid_ext).lower())
    