from unittest.mock import Mock, patch

from django.core.management import call_command
from django.db.models import FileField
from django.conf import settings
from django.test import TestCase, SimpleTestCase

from django_test_tools.assert_utils import write_assertions
from django_test_tools.file_utils import hash_file, temporary_file
from django_test_tools.management.commands.generate_factories import ModelFactoryGenerator
from django_test_tools.mixins import TestCommandMixin, TestOutputMixin
from django_test_tools.utils import create_output_filename_with_date


class TestGenerateFactories(TestOutputMixin, TestCommandMixin, TestCase):
    def test_generate_factories(self):
        call_command('generate_factories', 'example.servers', stdout=self.content)
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
        self.assertEqual(len(self.get_errors()), 10)


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
        call_command('generate_model_test_cases', 'example.servers', stdout=self.content)
        results = self.get_results()
        self.assertEqual(106, len(results))


class TestGenerateSerializersCommand(TestOutputMixin, TestCommandMixin, TestCase):
    def test_generate(self):
        call_command('generate_serializers', 'example.servers', stdout=self.content)
        results = self.get_results()
        self.assertEqual(22, len(results))


class TestCheckRequirementsCommand(TestCommandMixin, SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCheckRequirementsCommand, cls).setUpClass()
        cls.base_content = """# Wheel 0.25+ needed to install certain packages on CPython 3.5+
# like Pillow and psycopg2
# See http://bitly.com/wheel-building-fails-CPython-35
# Verified bug on Python 3.5.1
wheel==0.29.0

# Bleeding edge Django
django==1.11.3

# Configuration
django-environ==0.4.4


# Forms
django-braces==1.11.0
django-crispy-forms==1.6.1
django-floppyforms==1.7.0   """


    @temporary_file('txt', delete_on_exit=True)
    def test_check_requirements(self):
        requirement_file = self.test_check_requirements.filename
        with open(requirement_file, 'w', encoding='utf-8') as req_file:
            req_file.write(self.base_content)

        call_command('check_requirements', requirement_file, stdout=self.content)
        results = self.get_results()
        #write_assertions(results, 'results')
        #self.assertEqual(len(results), -1)
