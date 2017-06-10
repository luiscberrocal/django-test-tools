from django.apps.registry import apps

class DjangoAppManager(object):

    def __init__(self):
        self.installed_apps = dict(self.get_installed_apps())

    def get_app(self, app_name):
        return self.installed_apps.get(app_name)

    def get_installed_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config
