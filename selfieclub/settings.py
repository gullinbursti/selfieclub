"""
Django settings for selfieclub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'selfieclub-config')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 'SECRET_KEY' is in 'local_settings'
# SECRET_KEY =

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'media',
    'activity',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'selfieclub.urls'

WSGI_APPLICATION = 'selfieclub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'django': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(CONFIG_DIR, 'mysql-django.cnf'),
            'init_command': 'SET storage_engine=INNODB',
        },
    },
    'selfieclub': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(CONFIG_DIR, 'mysql-selfieclub.cnf'),
            'init_command': 'SET storage_engine=INNODB',
        },
    },
    # Leave this blank, we do not want a 'default' database defined.  Doing this as a safety so things dop not end up
    # strange places by accident.
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}


DATABASE_ROUTERS = [
    'selfieclub.dbrouters.DjangoDbRouter',
    'selfieclub.dbrouters.SelfieClubDbRouter',
    'selfieclub.dbrouters.FailDbRouter'
]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

AWS_S3_DIRECT_CLIENT_UPLOAD = {
    'bucket': 'volley-test',
    'acl': 'public-read',
    'url': 'https://volley-test.s3.amazonaws.com/',
    'expiry_minutes': 10
}

# Things that need to be in 'local_settings':
#     - SECRET_KEY
#     - AWS_CREDENTIALS
from local_settings import *
