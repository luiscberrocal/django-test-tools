from django.conf import settings
from django.test import TestCase

from django_test_tools.app_manager import DjangoAppManager


class TestDjangoAppManager(TestCase):
    def test_installed_apps(self):
        app_manager = DjangoAppManager()
        self.assertEqual(8, len(app_manager.installed_apps))

    def test_get_app(self):
        app_manager = DjangoAppManager()
        app = app_manager.get_app(settings.TEST_APP)
        self.assertEqual(settings.TEST_APP, app.name)

    def test_get_project_apps(self):
        app_manager = DjangoAppManager()
        app_module = settings.TEST_APP.split('.')[0]
        apps = app_manager.get_project_apps(app_module)
        self.assertEqual(1, len(apps))
        apps = app_manager.get_project_apps('django')
        self.assertEqual(6, len(apps))
