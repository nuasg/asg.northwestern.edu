"""
Django settings for asg project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'asg',
    'south',
    'tinymce',
    'colorfield',
    'easy_thumbnails',
    'image_cropping',
    'crispy_forms',
    'compressor',
    'easy_pdf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'asg.urls'

WSGI_APPLICATION = 'asg.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/uploads/'
MEDIA_ROOT = 'media'
MEDIAFILES_DIRS = (
    os.path.join(BASE_DIR, 'media'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Django auth LDAP

import ldap
from django_auth_ldap.config import LDAPSearch

AUTHENTICATION_BACKENDS = (
    'asg.auth.ASGLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = os.environ['NU_LDAP_URL']
AUTH_LDAP_BIND_DN = 'cn=asgnulink,ou=pwcheck,dc=northwestern,dc=edu'
AUTH_LDAP_BIND_PASSWORD = os.environ['NU_LDAP_PASSWORD']
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
    'username': 'uid',
}
AUTH_LDAP_ALWAYS_UPDATE_USER = False
AUTH_LDAP_BASE_DN = 'dc=northwestern,dc=edu'
AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_BASE_DN,
    ldap.SCOPE_SUBTREE, '(uid=%(user)s)')

# Django auth debugging code
#import logging
#logger = logging.getLogger('django_auth_ldap')
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.DEBUG)


# After login, send user to a custom view that checks the
# user type and redirects accordingly
LOGIN_REDIRECT_URL = 'asg.views.edit_profile'


# TinyMCE settings

TINYMCE_JS_URL = 'tinymce/tinymce.min.js'
TINYMCE_JS_ROOT = 'tinymce'
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'modern',
    'height': 400,
    'content_css': '/static/editor.css',
    'plugins': [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime table contextmenu paste'
    ],
    'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
}


# Django image cropping widget configuration

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

IMAGE_CROPPING_THUMB_SIZE = (300, 300)

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}


# Django crispy forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # add context processor for Django suit - new admin interface
    'django.core.context_processors.request',
    'asg.context_processors.my_senator',
)



try:
    from local_settings import *
except:
    pass
