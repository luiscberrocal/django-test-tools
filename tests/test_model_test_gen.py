from unittest import TestCase
from django.apps.registry import apps
from django_test_tools.file_utils import temporary_file, hash_file
from django_test_tools.generators.model_test_gen import ModelTestCaseGenerator, AppModelsTestCaseGenerator


class PythonWritingTestMixin:

    def write_generator_to_file(self, filename, generator):
        with open(filename, 'w', encoding='utf-8') as py_file:
            py_file.write(str(generator))
        hash = hash_file(filename)
        return hash


class TestModelTestCaseGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_str(self):
        app_name = 'example.my_app'
        model_name = 'Server'
        model = self._get_model(app_name, model_name)
        mtg = ModelTestCaseGenerator(model)
        hash = self.write_generator_to_file(self.test_str.filename, mtg)
        self.assertEqual('050f2cec39dd065ef004dd5ff057eba060d3cf80', hash)

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



class TestAppModelsTestCaseGenerator(PythonWritingTestMixin, TestCase):

    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = 'example.my_app'
        app = self._get_app(app_name)
        app_model_tests = AppModelsTestCaseGenerator(app)
        hash = self.write_generator_to_file(self.test_app_str.filename, app_model_tests)
        self.assertEqual('d4a0c7e3dd3b0154dab7560e0c450b0059940df5', hash)

    def _get_app(self, app_name):
        installed_apps = dict(self.get_apps())
        app = installed_apps.get(app_name)
        return app

    def get_apps(self):
        for app_config in apps.get_app_configs():
            yield app_config.name, app_config
