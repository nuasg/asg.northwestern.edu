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

TIME_ZONE = 'UTC'

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

"""
import ldap
from django_auth_ldap.config import LDAPSearch

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
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


## TODO debug
import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
## TODO debug
"""


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

try:
    from local_settings import *
except:
    pass
