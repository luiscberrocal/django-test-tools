from unittest import TestCase
from django.apps.registry import apps
from django_test_tools.file_utils import temporary_file, hash_file
from django_test_tools.generators.model_test_gen import ModelTestCaseGenerator, AppModelsTestCaseGenerator


class TestModelTestCaseGenerator(TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_str(self):
        app_name = 'example.my_app'
        model_name = 'Server'
        model = self._get_model(app_name, model_name)
        mtg = ModelTestCaseGenerator(model)
        with open(self.test_str.filename, 'w', encoding='utf-8') as py_file:
            py_file.write(str(mtg))
        hash = hash_file(self.test_str.filename)
        self.assertEqual('572bce38d1166cf9297397bd4ae5f0111cda6b86', hash)



    def _get_model(self, app_name, model_name):
        installed_apps = dict(self.get_apps())
        app = installed_apps.get(app_name)
        for model in app.get_models():
            if model_name == model.__name__:
                return model
        return None

    def get_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config



class TestAppModelsTestCaseGenerator(TestCase):

    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = 'example.my_app'
        app = self._get_app(app_name)
        app_model_tests = AppModelsTestCaseGenerator(app)
        with open(self.test_app_str.filename, 'w', encoding='utf-8') as py_file:
            py_file.write(str(app_model_tests))
        hash = hash_file(self.test_app_str.filename)
        self.assertEqual('9dff0316a97a411d2cc76d6b94316004074bc811', hash)

    def _get_app(self, app_name):
        installed_apps = dict(self.get_apps())
        app = installed_apps.get(app_name)
        return app

    def get_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config
