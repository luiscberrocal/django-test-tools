from unittest import TestCase

from django_test_tools.app_manager import DjangoAppManager
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
        app_name = 'example.servers'
        model_name = 'Server'
        app_manager = DjangoAppManager()
        model = app_manager.get_model(app_name, model_name)
        mtg = ModelTestCaseGenerator(model)
        hash = self.write_generator_to_file(self.test_str.filename, mtg)
        self.assertEqual(hash, '66ed114f8f2427ea4bdb17141fffb0741b9cd680')


class TestAppModelsTestCaseGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = 'example.servers'
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        app_model_tests = AppModelsTestCaseGenerator(app)
        hash = self.write_generator_to_file(self.test_app_str.filename, app_model_tests)
        self.assertEqual(hash, 'aa938222425fd4a5c704ed45c89f8053249cffe3')
