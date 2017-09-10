from django.apps.registry import apps


class DjangoAppManager(object):
    def __init__(self):
        self.installed_apps = dict(self.get_installed_apps())

    def get_app(self, app_name):
        return self.installed_apps.get(app_name)

    def get_installed_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config

    def get_model(self, app_name, model_name):
        app = self.get_app(app_name)
        for model in app.get_models():
            if model_name == model.__name__:
                return model
        return None

    def get_project_apps(self, project_name):
        project_apps = dict()
        for app_name, app_config in self.installed_apps.items():
            app_project = app_name.split('.')[0]
            if app_project == project_name:
                project_apps[app_name] = app_config
        return project_apps
