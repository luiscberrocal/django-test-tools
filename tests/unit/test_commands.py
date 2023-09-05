import json
from pathlib import Path
from unittest.mock import Mock, patch

from django.conf import settings
from django.core.management import call_command
from django.db.models import FileField
from django.test import TestCase, SimpleTestCase

from django_test_tools.assert_utils import write_assertions
from django_test_tools.file_utils import hash_file, temporary_file, create_dated
from django_test_tools.management.commands.generate_factories import ModelFactoryGenerator
from django_test_tools.mixins import TestCommandMixin, TestOutputMixin
from tests.common_vars import FIXTURES_FOLDER


class TestGenerateFactories(TestOutputMixin, TestCommandMixin, TestCase):
    def test_generate_factories(self):
        call_command('generate_factories', settings.TEST_APP_SERVERS, stdout=self.content)
        results = self.get_results()
        self.assertEqual(44, len(results))
        filename = create_dated('example_my_app_factory.py')
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


class TestAppToJSON(TestOutputMixin, TestCommandMixin, TestCase):
    def test_app_to_json(self):
        filename = Path(f'{settings.TEST_OUTPUT_PATH}/servers.json')
        call_command('app_to_json', settings.TEST_APP_SERVERS, filename=filename, stdout=self.content)
        results = self.get_results()

        self.assertEqual(len(results), 1)
        expected = f'Wrote dictionary to {filename}'
        self.assertEqual(results[0], expected)
        self.assertTrue(filename.exists())
        with open(filename, 'r') as f:
            file_dict = json.load(f)

        filename.unlink()
        # write_assertions(dictionary_list=file_dict, variable_name='file_dict')
        self.assertEqual(file_dict['app_name'], 'example.servers')
        self.assertEqual(len(file_dict['models']['operatingsystem']['fields']), 5)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][0]['editable'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][0]['field_name'], 'id')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][0]['help_text'], '')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][0]['primary_key'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][0]['type'], 'AutoField')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][0]['unique'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['editable'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['field_name'], 'name')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['help_text'], '')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['max_length'], 20)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['primary_key'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['type'], 'CharField')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][1]['unique'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['editable'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['field_name'], 'version')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['help_text'], '')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['max_length'], 5)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['primary_key'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['type'], 'CharField')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][2]['unique'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][3]['editable'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][3]['field_name'], 'licenses_available')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][3]['help_text'], '')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][3]['primary_key'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][3]['type'], 'IntegerField')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][3]['unique'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['decimal_places'], 2)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['editable'], True)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['field_name'], 'cost')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['help_text'], '')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['max_digits'], 7)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['primary_key'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['type'], 'DecimalField')
        self.assertEqual(file_dict['models']['operatingsystem']['fields'][4]['unique'], False)
        self.assertEqual(file_dict['models']['operatingsystem']['model_name'], 'OperatingSystem')
        self.assertEqual(len(file_dict['models']['operatingsystem']['original_attrs']['unique_together']), 2)
        self.assertEqual(file_dict['models']['operatingsystem']['original_attrs']['unique_together'][0], 'name')
        self.assertEqual(file_dict['models']['operatingsystem']['original_attrs']['unique_together'][1], 'version')
        self.assertEqual(len(file_dict['models']['server']['fields']), 11)
        self.assertEqual(file_dict['models']['server']['fields'][0]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][0]['field_name'], 'id')
        self.assertEqual(file_dict['models']['server']['fields'][0]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][0]['primary_key'], True)
        self.assertEqual(file_dict['models']['server']['fields'][0]['type'], 'AutoField')
        self.assertEqual(file_dict['models']['server']['fields'][0]['unique'], True)
        self.assertEqual(file_dict['models']['server']['fields'][1]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][1]['field_name'], 'name')
        self.assertEqual(file_dict['models']['server']['fields'][1]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][1]['max_length'], 20)
        self.assertEqual(file_dict['models']['server']['fields'][1]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][1]['type'], 'CharField')
        self.assertEqual(file_dict['models']['server']['fields'][1]['unique'], True)
        self.assertEqual(file_dict['models']['server']['fields'][2]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][2]['field_name'], 'notes')
        self.assertEqual(file_dict['models']['server']['fields'][2]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][2]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][2]['type'], 'TextField')
        self.assertEqual(file_dict['models']['server']['fields'][2]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][3]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][3]['field_name'], 'virtual')
        self.assertEqual(file_dict['models']['server']['fields'][3]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][3]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][3]['type'], 'BooleanField')
        self.assertEqual(file_dict['models']['server']['fields'][3]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][4]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][4]['field_name'], 'ip_address')
        self.assertEqual(file_dict['models']['server']['fields'][4]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][4]['max_length'], 39)
        self.assertEqual(file_dict['models']['server']['fields'][4]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][4]['type'], 'GenericIPAddressField')
        self.assertEqual(file_dict['models']['server']['fields'][4]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][5]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][5]['field_name'], 'created')
        self.assertEqual(file_dict['models']['server']['fields'][5]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][5]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][5]['type'], 'DateTimeField')
        self.assertEqual(file_dict['models']['server']['fields'][5]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][6]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][6]['field_name'], 'online_date')
        self.assertEqual(file_dict['models']['server']['fields'][6]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][6]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][6]['type'], 'DateField')
        self.assertEqual(file_dict['models']['server']['fields'][6]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][7]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][7]['field_name'], 'operating_system')
        self.assertEqual(file_dict['models']['server']['fields'][7]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][7]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][7]['remote_field'], 'OperatingSystem')
        self.assertEqual(file_dict['models']['server']['fields'][7]['type'], 'ForeignKey')
        self.assertEqual(file_dict['models']['server']['fields'][7]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][8]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][8]['field_name'], 'server_id')
        self.assertEqual(file_dict['models']['server']['fields'][8]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][8]['max_length'], 6)
        self.assertEqual(file_dict['models']['server']['fields'][8]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][8]['type'], 'CharField')
        self.assertEqual(file_dict['models']['server']['fields'][8]['unique'], False)
        self.assertEqual(len(file_dict['models']['server']['fields'][9]['choices']), 2)
        self.assertEqual(len(file_dict['models']['server']['fields'][9]['choices'][0]), 2)
        self.assertEqual(file_dict['models']['server']['fields'][9]['choices'][0][0], 'PROD')
        self.assertEqual(file_dict['models']['server']['fields'][9]['choices'][0][1], 'Prod')
        self.assertEqual(len(file_dict['models']['server']['fields'][9]['choices'][1]), 2)
        self.assertEqual(file_dict['models']['server']['fields'][9]['choices'][1][0], 'DEV')
        self.assertEqual(file_dict['models']['server']['fields'][9]['choices'][1][1], 'Dev')
        self.assertEqual(file_dict['models']['server']['fields'][9]['choices_type'], 'tuple')
        self.assertEqual(file_dict['models']['server']['fields'][9]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][9]['field_name'], 'use')
        self.assertEqual(file_dict['models']['server']['fields'][9]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][9]['max_length'], 4)
        self.assertEqual(file_dict['models']['server']['fields'][9]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][9]['type'], 'CharField')
        self.assertEqual(file_dict['models']['server']['fields'][9]['unique'], False)
        self.assertEqual(file_dict['models']['server']['fields'][10]['editable'], True)
        self.assertEqual(file_dict['models']['server']['fields'][10]['field_name'], 'comments')
        self.assertEqual(file_dict['models']['server']['fields'][10]['help_text'], '')
        self.assertEqual(file_dict['models']['server']['fields'][10]['primary_key'], False)
        self.assertEqual(file_dict['models']['server']['fields'][10]['type'], 'TextField')
        self.assertEqual(file_dict['models']['server']['fields'][10]['unique'], False)
        self.assertEqual(file_dict['models']['server']['model_name'], 'Server')

        # print(results)


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
        #        import environ
        output = self.test_excel_to_json.filename
        # excel_file = (environ.Path(__file__) - 1).path('fixtures', 'excel_to_json.xlsx').root
        excel_file = FIXTURES_FOLDER / 'excel_to_json.xlsx'
        call_command('convert_to_json', input=excel_file, output=output,
                     stdout=self.content)
        hash_digest = hash_file(output)
        app_name = settings.TEST_APP_SERVERS
        if app_name == 'example.servers':
            self.assertEqual(hash_digest, '535ffac988e95a1536fe6803ea7d78c99b1c28df')
        else:
            self.assertEqual(hash_digest, '535ffac988e95a1536fe6803ea7d78c99b1c28df')
