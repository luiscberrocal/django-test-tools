from unittest import TestCase

from django.conf import settings

from django_test_tools.app_manager import DjangoAppManager
from django_test_tools.file_utils import temporary_file, hash_file, compare_content
from django_test_tools.generators.model_test_gen import ModelTestCaseGenerator, AppModelsTestCaseGenerator
from tests.common_vars import FIXTURES_FOLDER


class PythonWritingTestMixin:

    def write_generator_to_file(self, filename, generator):
        # FIXME Deprecate
        with open(filename, 'w', encoding='utf-8') as py_file:
            py_file.write(str(generator))
        hash = hash_file(filename)
        return hash


class TestModelTestCaseGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_str_servers(self):
        app_name = settings.TEST_APP_SERVERS
        model_name = 'Server'
        app_manager = DjangoAppManager()
        model = app_manager.get_model(app_name, model_name)
        mtg = ModelTestCaseGenerator(model)

        test_file = self.test_str_servers.filename
        self.write_generator_to_file(test_file, mtg)

        source_file = FIXTURES_FOLDER / 'test_app_str_20230903_0820.py'

        errors = compare_content(source_file=source_file, test_file=test_file, raise_exception=False)
        self.assertEqual(len(errors), 0)


class TestAppModelsTestCaseGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_app_str_servers(self):
        app_name = settings.TEST_APP_SERVERS
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        app_model_tests = AppModelsTestCaseGenerator(app)
        self.write_generator_to_file(self.test_app_str_servers.filename, app_model_tests)
        source_file = FIXTURES_FOLDER / 'test_app_str_servers_20230904_0746.py'

        errors = compare_content(source_file=source_file, test_file=self.test_app_str_servers.filename,
                                 raise_exception=False)
        self.assertEqual(len(errors), 0)
