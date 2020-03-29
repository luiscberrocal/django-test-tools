from .settings import *

TEST_APP_SERVERS = 'servers'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_test_tools',
    TEST_APP_SERVERS,
    # if your app has other dependencies that need to be added to the site
    # they should be added here
]
ROOT_URLCONF = 'example.urls'
