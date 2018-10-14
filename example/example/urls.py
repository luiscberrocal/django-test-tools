"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django import VERSION as django_version
if django_version >= (2, 0):
    from django.urls import path
else:
    from django.conf.urls import url

if django_version >= (2, 0):
    urlpatterns = [
        path(r'admin/', admin.site.urls),
        path(r'', include('django_test_tools.urls')),
    ]
else:
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'', include('django_test_tools.urls', namespace='django_test_tools')),
    ]
