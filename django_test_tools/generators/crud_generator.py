


class UrlGenerator(object):
    URL_CRUD_TEMPLATE = """# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import {0}ListView, {0}CreateView, {0}UpdateView, {0}DeleteView, {0}DetailView

urlpatterns = [
    url(r'^$', {0}ListView.as_view(), name='list'),
    url(r'^create/$', {0}CreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', {0}UpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', {0}DeleteView.as_view(), name='delete'),
    url(r'^detail/(?P<pk>\d+)/$', {0}DetailView.as_view(), name='detail'),
]"""

    def __init__(self, model_name):
        self.model_name = model_name

    def print_urls(self, filename):
        with open(filename, 'w', encoding='utf-8') as url_file:
            url_file.write(self.URL_CRUD_TEMPLATE.format(self.model_name))
