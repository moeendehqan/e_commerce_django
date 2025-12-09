from PIL import Image
import os




def convert_to_webp(instance, field_name):
    """
    تبدیل تصویر به فرمت WebP
    
    :param instance: نمونه مدل
    :param field_name: نام فیلد تصویر
    :return: مسیر نسبی فایل WebP
    """
    field = getattr(instance, field_name)
    
    # اگر تصویری وجود نداشته باشد، خارج می‌شویم
    if not field:
        return None
    
    # باز کردن تصویر با Pillow
    img = Image.open(field.path)
    
    # تعیین نام فایل جدید با پسوند .webp
    file_name, _ = os.path.splitext(os.path.basename(field.name))
    webp_file_name = f"{file_name}.webp"
    webp_path = os.path.join(os.path.dirname(field.path), webp_file_name)
    
    # ذخیره تصویر با فرمت WebP
    img.save(webp_path, 'WEBP', quality=85)
    
    # مسیر نسبی فایل WebP
    webp_relative_path = os.path.join(os.path.dirname(field.name), webp_file_name)
    
    # حذف فایل اصلی اگر پسوند آن متفاوت است
    if os.path.basename(field.path) != webp_file_name:
        if os.path.exists(field.path):
            os.remove(field.path)
    
    return webp_relative_path