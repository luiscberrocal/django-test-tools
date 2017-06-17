import os

from django.conf import settings
from django.template.loader import render_to_string

from ..app_manager import DjangoAppManager


def create_folder_structure(doc_base_folder, project_name):
    #print('**** APP_DIR {} ****'.format(settings.APPS_DIR))
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
        template = 'django_test_tools/app_index.rst.j2'
        write_template(data, folder, 'index.rst',template)
        data = {
            'verbose_name': str(app.verbose_name),
            'module_name': '{}.models'.format(app_name)
        }
        template = 'django_test_tools/app_module.rst.j2'
        write_template(data, folder, '{}.models.rst'.format(app_name), template)



def get_module_files(folder):
    file_black_list = ['__init__.py', 'urls.py']
    folder_black_list = ['tests', 'migrations']
    file_list = list()
    package_name = ''
    for root, dirs, files in os.walk(folder):
        base_folder_name = os.path.split(root)[1]
        if base_folder_name not in folder_black_list:
            if '__init__.py' in files:
                package_name = package_name + '.' + base_folder_name
            for file in files:
                if file.endswith('.py'):
                    module_name = file.split('.')[0]
                    if file not in file_black_list:
                        module_dict = dict()
                        module_dict['filename'] = os.path.join(root,file)
                        module_dict['package_name'] = (package_name + '.{}'.format(module_name))[1:]
                        file_list.append(module_dict)
        else:
            del dirs[:]
    return file_list




def write_template(data, folder, output_file, template):
    rendered = render_to_string(template, data)
    index_filename = os.path.join(folder, output_file)
    with open(index_filename, 'w', encoding='utf-8') as index_file:
        index_file.write(rendered)




