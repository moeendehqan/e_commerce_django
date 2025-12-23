from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

def convert_to_webp(instance, field_name):
    """
    Convert image to WebP format.
    
    :param instance: Model instance
    :param field_name: Image field name
    :return: Relative path of the WebP file
    """
    field = getattr(instance, field_name)
    
    # If no image, return None
    if not field:
        return None
    
    # Check if already WebP (by extension)
    if field.name.lower().endswith('.webp'):
        return None

    try:
        # Open image using storage API
        field.open()
        img = Image.open(field)
        
        # Convert to WebP in memory
        image_io = BytesIO()
        img.save(image_io, format='WEBP', quality=85)
        image_io.seek(0)
        
        # Determine new filename
        file_name = os.path.splitext(os.path.basename(field.name))[0]
        webp_file_name = f"{file_name}.webp"
        
        # Determine new path (handling S3/MinIO paths which use forward slashes)
        dir_name = os.path.dirname(field.name)
        webp_path = os.path.join(dir_name, webp_file_name).replace('\\', '/')
        
        # Save new file to storage
        field.storage.save(webp_path, ContentFile(image_io.read()))
        
        # Delete old file if name is different
        if field.name != webp_path:
             field.storage.delete(field.name)
             
        return webp_path

    except Exception as e:
        print(f"Error converting to WebP: {e}")
        return None
