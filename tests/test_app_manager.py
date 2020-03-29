from django.conf import settings
from django.test import TestCase

from django_test_tools.app_manager import DjangoAppManager
from django_test_tools.assert_utils import write_assertions


class TestDjangoAppManager(TestCase):
    def test_installed_apps(self):
        app_manager = DjangoAppManager()
        self.assertEqual(8, len(app_manager.installed_apps))

    def test_get_app(self):
        app_manager = DjangoAppManager()
        app = app_manager.get_app(settings.TEST_APP_SERVERS)
        self.assertEqual(settings.TEST_APP_SERVERS, app.name)
        self.assertEqual('example.servers', app.name)
        self.assertEqual(app.models['server'].__name__, 'server')
        self.assertEqual(len(app.models['server']._meta.fields), 11)
        self.assertEqual(app.models['server']._meta.fields[0].name, 'id')
        self.assertEqual(type(app.models['server']._meta.fields[0].name).__name__, 'id')

    def test_get_project_apps(self):
        app_manager = DjangoAppManager()
        app_module = settings.TEST_APP_SERVERS.split('.')[0]
        apps = app_manager.get_project_apps(app_module)
        self.assertEqual(1, len(apps))
        apps = app_manager.get_project_apps('django')
        self.assertEqual(6, len(apps))

    def test_get_app(self):
        app_manager = DjangoAppManager()
        app_dict = app_manager.get_app_data(settings.TEST_APP_SERVERS)
        #write_assertions(app_dict, 'app_dict')

