import os
from unittest import mock
from unittest.mock import Mock, patch

from django.conf import settings
from django.core.management import call_command
from django.db.models import FileField
from django.test import TestCase, SimpleTestCase

from django_test_tools.file_utils import hash_file, temporary_file
from django_test_tools.management.commands.generate_factories import ModelFactoryGenerator
from django_test_tools.mixins import TestCommandMixin, TestOutputMixin
from django_test_tools.utils import create_output_filename_with_date


class TestGenerateFactories(TestOutputMixin, TestCommandMixin, TestCase):
    def test_generate_factories(self):
        call_command('generate_factories', settings.TEST_APP_SERVERS, stdout=self.content)
        results = self.get_results()
        self.assertEqual(44, len(results))
        filename = create_output_filename_with_date('example_my_app_factory.py')
        with open(filename, 'w', encoding='utf-8') as factory_file:
            for line in results:
                factory_file.write(line)
                factory_file.write('\n')
        hash_sha = hash_file(filename, algorithm='sha256')
        self.assertEqual('c8c331856529fe10afe8460de8dbd04b5f208d2a4922c275c1f6309bf7a3ed95', hash_sha)
        self.clean_output_folder(filename)

    def test_generate_factories_error(self):
        call_command('generate_factories', 'invalid_name', stdout=self.content, stderr=self.error_content)
        results = self.get_results()
        self.assertEqual(len(results), 0)
        self.assertEqual(len(self.get_errors()), 11)


class FileFieldMockType(object):
    field_name = None

    # noinspection PyShadowingBuiltins
    def __init__(cls, what, bases=None, dict=None):
        cls.__name__ = 'FileField'


class TestModelFactoryGenerator(TestCase):
    def test__generate_file_field(self):
        field = Mock(spec=FileField)
        field.name = 'hola'
        # self.assertEqual('', type(field).__name__)
        mock_model = Mock()
        mock_model.__name__ = 'SuperModel'
        mock_model._meta = Mock()
        mock_model._meta.fields = [field]
        factory_gen = ModelFactoryGenerator(mock_model)

        with patch('builtins.type', FileFieldMockType) as m_type:
            results = factory_gen._generate()
            field_definition = results[1]['print'].format(*results[1]['args'])
            self.assertEqual('    hola = FileField(filename=\'hola.xlsx\')', field_definition)
            self.assertEqual('    {} = FileField(filename=\'{}.{}\')', results[1]['print'])
            self.assertEqual(['hola', 'hola', 'xlsx'], results[1]['args'])


class TestGenerateModelTestCasesCommand(TestOutputMixin, TestCommandMixin, TestCase):
    def test_generate(self):
        call_command('generate_model_test_cases', settings.TEST_APP_SERVERS, stdout=self.content)
        results = self.get_results()
        self.assertEqual(106, len(results))


class TestGenerateSerializersCommand(TestOutputMixin, TestCommandMixin, TestCase):
    def test_generate(self):
        call_command('generate_serializers', settings.TEST_APP_SERVERS, stdout=self.content)
        results = self.get_results()
        self.assertEqual(22, len(results))



# class TestGitReportCommand(TestCommandMixin, SimpleTestCase):
#
#     @temporary_file('xlsx', delete_on_exit=True)
#     def test_command_git_report(self):
#         output = b'"552472e|github-bot@pyup.io|2018-10-01 10:16:27 -0500|Update django from 2.0.7 to 2.1.2"\n' \
#                  b'"bbb1c9e|github-bot@pyup.io|2018-10-01 10:16:26 -0500|Update django from 2.0.7 to 2.1.2"\n' \
#                  b'"8d3e049|luis.berrocal.1942@gmail.com|2018-09-25 20:44:39 -0500|Merge pull request #51 from luiscberrocal/pyup-update-openpyxl-2.5.4-to-2.5.8"\n' \
#                  b'"07f2ef3|github-bot@pyup.io|2018-09-25 12:36:13 -0500|Update openpyxl from 2.5.4 to 2.5.8"\n' \
#                  b'"b319f74|luis.berrocal.1942@gmail.com|2018-09-23 10:37:30 -0500|Merge pull request #50 from luiscberrocal/pyup-update-faker-0.8.17-to-0.9.1"\n' \
#                  b'"166c5b0|unknown@example.com|2018-09-23 09:40:44 -0500|Merge branch \'release/1.1.2\'"\n' \
#                  b'"98e74fb|unknown@example.com|2018-09-23 09:40:43 -0500|Merge branch \'release/1.1.2\' into develop"\n' \
#                  b'"cb0c110|luis.berrocal.1942@gmail.com|2018-09-23 09:40:16 -0500|Bump version: 1.1.1 -> 1.1.2"\n' \
#                  b'"5ca8421|github-bot@pyup.io|2018-09-23 09:39:23 -0500|Update faker from 0.8.17 to 0.9.1"\n' \
#                  b'"2fbee22|luis.berrocal.1942@gmail.com|2018-09-23 09:37:50 -0500|Updated requirements"\n'
#
#         mock_capture = mock.Mock()
#         mock_capture.return_value = output
#         filename = self.test_command_git_report.filename
#         with mock.patch('django_test_tools.pip.utils.subprocess.check_output', mock_capture):
#             call_command('git_report', filename=filename, stdout=self.content)
#             results = self.get_results()
#             self.assertEqual(len(results), 12)
#             self.assertEqual(results[0],
#                              '552472e|github-bot@pyup.io|2018-10-01 10:16:27 -0500|Update django from 2.0.7 to 2.1.2')
#             self.assertEqual(results[-2], '')
#             self.assertEqual(results[-3],
#                              '2fbee22|luis.berrocal.1942@gmail.com|2018-09-23 09:37:50 -0500|Updated requirements')
#
#         self.assertTrue(os.path.exists(filename))

    # @temporary_file('xlsx', delete_on_exit=True)
    # def test_(self):
    #     filename = self.test_.filename
    #     call_command('git_report', filename=filename, stdout=self.content)
    #


class TestSerializerTestGeneratorCommand(TestCommandMixin, SimpleTestCase):

    @temporary_file('py', delete_on_exit=True)
    def test_generate_serializers_tests(self):
        filename = self.test_generate_serializers_tests.filename
        try:
            call_command('generate_serializers_tests',
                         'servers.api.serializers.ServerSerializer',
                         filename=filename, stdout=self.content)
        except Exception:
            call_command('generate_serializers_tests',
                         'example.servers.api.serializers.ServerSerializer',
                         filename=filename, stdout=self.content)

        results = self.get_results()
        self.assertTrue('Printed to file' in results[0])


class TestConvertToJSONCommand(TestCommandMixin, SimpleTestCase):

    @temporary_file('json', delete_on_exit=True)
    def test_excel_to_json(self):
        import environ
        output = self.test_excel_to_json.filename
        excel_file = (environ.Path(__file__) - 1).path('fixtures', 'excel_to_json.xlsx').root
        call_command('convert_to_json', input=excel_file, output=output,
                     stdout=self.content)
        hash = hash_file(output)
        app_name = settings.TEST_APP_SERVERS
        if app_name == 'example.servers':
            self.assertEqual(hash, '535ffac988e95a1536fe6803ea7d78c99b1c28df')
        else:
            self.assertEqual(hash, '535ffac988e95a1536fe6803ea7d78c99b1c28df')
