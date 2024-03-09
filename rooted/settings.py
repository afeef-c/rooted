"""
Django settings for rooted project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY='django-insecure-6s+idmt@&+*i3d-)g+g+ls6a$g+sf%gxv%td#yo_n=cn9*zkjx'
DEBUG=False


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG', default=True)
SECRET_KEY = 'django-insecure-6s+idmt@&+*i3d-)g+g+ls6a$g+sf%gxv%td#yo_n=cn9*zkjx'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=True, cast=bool)

DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #custom apps
    'category',
    'accounts',
    'store',
    'cart',
    'orders',
    
    'customadmin',
    #'admin_honeypot',
    
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #custome middleware
    # for restric logged user to login page
    'accounts.middleware.RedirectAuthenticatedUserMiddleware',
    #restrict blocked user
    'rooted.middleware.BlockedUserMiddleware',


    'corsheaders.middleware.CorsMiddleware', 
    
]

ROOT_URLCONF = 'rooted.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'cart.context_processors.counter',
                'cart.context_processors.cart',
                'accounts.context_processors.w_counter',
                'accounts.context_processors.wishlist',
            ],
        },
    },
]

WSGI_APPLICATION = 'rooted.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
        
#    }
#}



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rootedplants',
        'USER': 'afeefc123',
        'PASSWORD': 'ummerc123!',
        'HOST': 'rootedplants.cfs8kyc4kwl3.eu-north-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'




# SMTP Email settings
# EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'afeefc123@gmail.com'
EMAIL_HOST_PASSWORD = 'kgaa gfwy rfzj nhtx'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='afeefc123@gmail.com'
EMAIL_HOST_PASSWORD='kgaa gfwy rfzj nhtx'
EMAIL_USE_SSL=False


#PAYPAL_RECEIVER_EMAIL = 'rootedstores@gmail.com'
#PAYPAL_TEST = True

# RAZOR_KEY_ID = config('RAZOR_KEY_ID')

RAZOR_KEY_ID = 'rzp_test_VlrhibhaWWTpKb'
RAZOR_KEY_SECRET = 'bSbPSE4eWm0lZdf6PgsijdEW'


# To Enable Popus in Django or else it will block the payment popup
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

CORS_ORIGIN_ALLOW_ALL = True  



AWS_ACCESS_KEY_ID = 'AKIAQ3EGTSLPSGMOV433'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'rootedplants'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


