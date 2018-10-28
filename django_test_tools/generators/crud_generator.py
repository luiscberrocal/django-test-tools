from django.template.loader import render_to_string


class UrlGenerator(object):

    def __init__(self, model_name):
        self.model_name = model_name
        self.template = 'django_test_tools/urls.py.j2'

    def print_urls(self, filename):
        data = dict()
        data['model_name'] = self.model_name
        data['print_urls'] = True
        rendered = render_to_string(self.template, data)
        with open(filename, 'w', encoding='utf-8') as url_file:
            url_file.write(rendered)

    def print_paths(self, filename):
        data = dict()
        data['model_name'] = self.model_name
        data['print_paths'] = True
        rendered = render_to_string(self.template, data)
        with open(filename, 'w', encoding='utf-8') as url_file:
            url_file.write(rendered)
