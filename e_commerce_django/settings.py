import os
from pathlib import Path
AUTH_USER_MODEL = 'user.User'

BASE_DIR = Path(__file__).resolve().parent.parent


AUTH_USER_MODEL = 'user.User'
SECRET_KEY = 'django-insecure-l3#rjax53)!h!=q!m(y(r_=k)b(xmwvk@q3_8lo70d$j8f!6#)'


DEBUG = os.environ.get('DEBUG','False').lower() == 'true'

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "https://shopsepid.ir,https://www.shopsepid.ir").split(",")
SITE_ID = 1

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'user',
    'product',
    'order',
    'core',
    'blog',
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]



ROOT_URLCONF = 'e_commerce_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.basket_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_commerce_django.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB','echr'),
        'USER': os.environ.get('POSTGRES_USER','admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD','Moeen....6168'),
        'HOST': os.environ.get('POSTGRES_HOST','193.56.135.13'),
        'PORT': os.environ.get('POSTGRES_PORT','5432'),
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
APPEND_SLASH = True
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'brand_colour': 'navbar-dark',
    'logo': 'https://yourlogo.com/logo.png',
    'brand_text': 'پنل مدیریت',

}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },

    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}