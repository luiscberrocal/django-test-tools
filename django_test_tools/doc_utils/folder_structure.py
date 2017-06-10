import os

from django.conf import settings
from django.template.loader import render_to_string

from ..app_manager import DjangoAppManager


def create_folder_structure(doc_base_folder, project_name):
    print('**** APP_DIR {} ****'.format(settings.APPS_DIR))
    app_manager = DjangoAppManager()
    project_apps = app_manager.get_project_apps(project_name)
    project_folder = os.path.join(doc_base_folder, project_name)
    for app_name, app in project_apps.items():
        folder = os.path.join(project_folder, app.label)
        if not os.path.exists(folder):
            os.makedirs(folder)
        data ={
            'verbose_name': str(app.verbose_name),
            'app_package': app_name
        }
        rendered = render_to_string('django_test_tools/app_index.rst.j2', data)
        index_filename = os.path.join(folder, 'index.rst')
        with open(index_filename, 'w', encoding='utf-8') as index_file:
            index_file.write(rendered)



