from django.core.exceptions import ValidationError
import os


def allow_only_images(value):
    ext=os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions=['.jpg','.jpeg','.png']    
    if  not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Allowed extensions are: .jpg, .jpeg, .png")