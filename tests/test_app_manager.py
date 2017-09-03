from django.test import TestCase

from django_test_tools.app_manager import DjangoAppManager


class TestDjangoAppManager(TestCase):
    def test_installed_apps(self):
        app_manager = DjangoAppManager()
        self.assertEqual(8, len(app_manager.installed_apps))

    def test_get_app(self):
        app_manager = DjangoAppManager()
        app = app_manager.get_app('example.servers')
        self.assertEqual('example.servers', app.name)

    def test_get_project_apps(self):
        app_manager = DjangoAppManager()
        apps = app_manager.get_project_apps('example')
        self.assertEqual(1, len(apps))
        apps = app_manager.get_project_apps('django')
        self.assertEqual(6, len(apps))
