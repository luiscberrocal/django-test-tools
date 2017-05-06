
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.db.models import Field
from django.db.models import FileField
from django.test import TestCase

from django_test_tools.management.commands.generate_factories import ModelFactoryGenerator
from django_test_tools.mixins import TestCommandMixin


class TestGenerateFactories(TestCommandMixin, TestCase):

    def test_generate(self):
        call_command('generate_factories', 'example.my_app', stdout=self.content)
        results = self.get_results()
        self.assertEqual(41, len(results))

class MockType(object):

    def __init__(cls, what, bases=None, dict=None): # known special case of type.__init__
        """
        type(object_or_name, bases, dict)
        type(object) -> the object's type
        type(name, bases, dict) -> a new type
        # (copied from class doc)
        """
        if dict:
            field_name = dict.get('field_name')
        cls.__name__ = 'FileField'


class TestModelFactoryGenerator(TestCase):


    def test__generate(self):
        field = Mock(spec=FileField)
        field.name = 'hola'
        #self.assertEqual('', type(field).__name__)
        mock_model = Mock()
        mock_model.__name__ = 'SuperModel'
        mock_model._meta = Mock()
        mock_model._meta.fields = [field]
        factory_gen = ModelFactoryGenerator(mock_model)

        with  patch('builtins.type', MockType) as m_type:
            results = factory_gen._generate()
            self.assertEqual('    {} = FileField(filename=\'{}.{}\')', results[1]['print'])
            self.assertEqual(['hola', 'hola', 'xlsx'], results[1]['args'])
