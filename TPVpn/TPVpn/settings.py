#    -*- coding: UTF-8 -*-
#
#    --- License block --------------------------------------------------------
#    This file is part of TPVpn.
#
#    TPVpn is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TPVpn is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TPVpn.  If not, see <http://www.gnu.org/licenses/>.
#    --- End of License block -------------------------------------------------


"""
Django settings for TPVpn project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p_%m*r$+%+e9)+$mgm=txinz#m5(e#&$6mgux*s#)sk)8h-l(j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TPVpnapp',
    'rest_framework',
    'corsheaders',
    'django_tables2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # EVITAR PROBLEMAS CSRF
    'TPVpnapp.disableCSRF.DisableCSRF',
    'TPVpnapp.django-crossdomainxhr-middleware.XsSharing',
    'corsheaders.middleware.CorsMiddleware',
    'TPVpnapp.utils.ThreadLocalMiddleware',
)

ROOT_URLCONF = 'TPVpn.urls'
STATIC_ROOT = os.path.join(BASE_DIR, "TPVpn/static/")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['TPVpn/static/common/templates'],
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

WSGI_APPLICATION = 'TPVpn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'root',
        'PASSWORD': 'qw78zx12',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Serializer to work with Angular
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    'TPVpn/static/common',
)


MEDIA_ROOT = os.path.join(BASE_DIR, 'TPVpn/media/')
MEDIA_URL = '/media/'
'''
MEDIAFILES_DIRS = (
    'TPVpn/media',
)
'''
# MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
# )
# MEDIA_URL = '/media/'
# MEDIA_ROOT = (
#    'TPVpn/media',
# )
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True
'''
CORS_ORIGIN_WHITELIST = [
    '127.0.0.1:8000',
    '0.0.0.0:8001',
    '127.0.0.1:8001',
    '192.168.1.37:8001'
]
'''
CORS_ALLOW_CREDENTIALS = True

EMAIL_USE_TLS = True
EMAIL_SENDER = 'blabla@gmail.es'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'blabla@gmail.es'
EMAIL_HOST_PASSWORD = 'blabla'
EMAIL_PORT = 587
