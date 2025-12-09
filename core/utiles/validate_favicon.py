

import os

def validate_favicon(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.ico':
        raise ValidationError('فایکون باید با پسوند .ico باشد')

    if value.size > 1024 * 1024: 
        raise ValidationError('حجم فایل فایکون نباید بیشتر از 1 مگابایت باشد')