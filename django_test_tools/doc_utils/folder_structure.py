import os

from ..app_manager import DjangoAppManager


def create_folder_structure(doc_base_folder, project_name):
    app_manager = DjangoAppManager()
    project_apps = app_manager.get_project_apps(project_name)
    project_folder = os.path.join(doc_base_folder, project_name)
    for app_name, app in project_apps.items():
        folder = os.path.join(project_folder, app.label)
        if not os.path.exists(folder):
            os.makedirs(folder)


