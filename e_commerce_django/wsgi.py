

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce_django.settings')

application = get_wsgi_application()
