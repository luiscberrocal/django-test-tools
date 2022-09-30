# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

try:
    from django.conf.urls import url

    urlpatterns = [
        url(r'', TemplateView.as_view(template_name="base.html")),
    ]
except:
    from django.urls import path

    urlpatterns = [
        path('', TemplateView.as_view(template_name="base.html")),
    ]
