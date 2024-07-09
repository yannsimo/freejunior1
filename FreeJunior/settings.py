"""
Django settings for FreeJunior_version1 project.

Generated by 'django-admin startproject' using Django 5.0.6.

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
SECRET_KEY = 'django-insecure-ftr+!#=(zmff91&956_x#vdhxdh@&#vc5sx*6-7rc(4h$lbdub'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['54.87.17.222']
ALLOWED_HOSTS = ['127.0.0.1']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'StudentApp.apps.StudentappConfig',
     'bootstrap4',
    'Accounts.apps.AccountsConfig',
]
AUTH_USER_MODEL = 'Accounts.User'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'FreeJunior.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FreeJunior.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'freejuniordatabase',
        'USER': 'yann',
        'PASSWORD': 'Lavitesse123*',
        'HOST': 'freejuniordatabase.cnu228qegvai.us-east-1.rds.amazonaws.com',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




AWS_ACCESS_KEY_ID = 'AKIA4MTWNWMLZ4KXQEUX'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'django-freejunior'


STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Configurations pour les fichiers média
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# settings.py
LOGIN_REDIRECT_URL = 'home'  # Page où l'utilisateur sera redirigé après la connexion
LOGOUT_REDIRECT_URL = 'login'  # Page où l'utilisateur sera redirigé après la déconnexion

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'yannjuniorsim@gmail.com'
EMAIL_HOST_PASSWORD = 'vnyranwgtptuhrcm'