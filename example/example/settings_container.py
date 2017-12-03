from .settings import *

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_test_tools.apps.DjangoTestToolsConfig',
    'servers',

    # if your app has other dependencies that need to be added to the site
    # they should be added here
]
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'
