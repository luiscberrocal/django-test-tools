import importlib
import os
from django.test import TestCase, SimpleTestCase

from django_test_tools.file_utils import hash_file, temporary_file
from django_test_tools.generators.crud_generator import UrlGenerator, SerializerTestGenerator
# try:
#     from example.servers.api.serializers import ServerSerializer
# except:
#     from servers.api.serializers import ServerSerializer


class TestUrlGenerator(TestCase):

    @temporary_file('.py', delete_on_exit=True)
    def test_print_urls(self):
        filename = self.test_print_urls.filename
        generator = UrlGenerator('Server')
        generator.print_urls(filename)
        self.assertTrue(os.path.exists(filename))
        hash = hash_file(filename)
        self.assertEqual(hash, '14ef340ea846e3d37fd71d80362a5225e05133a3')

    @temporary_file('.py', delete_on_exit=True)
    def test_print_paths(self):
        filename = self.test_print_paths.filename
        generator = UrlGenerator('Server')
        generator.print_paths(filename)
        self.assertTrue(os.path.exists(filename))
        hash = hash_file(filename)
        self.assertEqual(hash, 'de4251b6c78a5911b6c3440c580de05d4d417c59')


class TestSerializerTestGenerator(SimpleTestCase):

    @temporary_file('.py', delete_on_exit=False)
    def test_print(self):
        filename = self.test_print.filename
        generator = SerializerTestGenerator()
        data= dict()
        try:
            my_module = importlib.import_module("servers.api.serializers")
        except:
            my_module = importlib.import_module("example.servers.api.serializers")
        ServerSerializer = getattr(my_module, "ServerSerializer")

        serializer = ServerSerializer()
        rep_ser = repr(serializer)
        fields = list()
        str_fields = list()
        for field in serializer.fields:
            fields.append(field)

        for key, field in serializer.fields.fields.items():
            if type(field).__name__ in ['CharField', 'TextField']:
                str_fields.append(field.field_name)
            print(key)

        data['model_name'] = serializer.Meta.model.__name__
        data['fields'] = fields
        data['string_vars'] = str_fields
        generator.print(data, filename)
        hash = hash_file(filename)
        self.assertEqual(hash, 'a6961c9294f5acc02350835596faa3c38ee266df')
