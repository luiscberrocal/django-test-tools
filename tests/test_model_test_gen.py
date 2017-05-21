from unittest import TestCase
from django.apps.registry import apps
from django_test_tools.file_utils import temporary_file, hash_file
from django_test_tools.generators.model_test_gen import ModelTestCaseGenerator


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
        self.assertEqual('811265df91212485186f84ae73fba5dc85367f04', hash)



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
