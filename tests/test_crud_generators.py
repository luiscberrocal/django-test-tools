import importlib
import os

from django.conf import settings
from django.test import TestCase, SimpleTestCase

from django_test_tools.file_utils import hash_file, temporary_file
from django_test_tools.generators.crud_generator import UrlGenerator, SerializerTestGenerator, GenericTemplateWriter


# try:
#     from example.servers.api.serializers import ServerSerializer
# except:
#     from servers.api.serializers import ServerSerializer
from django_test_tools.generators.model_generator import FactoryBoyGenerator


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

    @temporary_file('.py', delete_on_exit=True)
    def test_print(self):
        filename = self.test_print.filename
        generator = SerializerTestGenerator()
        data = dict()
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
        self.assertEqual(hash, '7ef21355fba29674cadb111e6217b1ed100d5e5a')

    @temporary_file('.py', delete_on_exit=True)
    def test_print_snake_case(self):
        filename = self.test_print_snake_case.filename
        generator = SerializerTestGenerator()
        data = dict()
        fields = ['name', 'power']
        str_fields = ['name']

        data['model_name'] = 'ComplicatedObject'
        data['fields'] = fields
        data['string_vars'] = str_fields
        generator.print(data, filename)
        hash = hash_file(filename)
        self.assertEqual(hash, 'b635eaef01ce567e83fd5700a5888e783caf3c6e')


class TestGenericTemplateWriter(SimpleTestCase):
    #
    # @temporary_file('.py', delete_on_exit=True)
    # def test_write(self):
    #     factory_data = dict()
    #     factory_data['factories'] = list()
    #     factory = dict()
    #     factory['model_name'] = 'Server'
    #     factory['attributes'] = list()
    #     attribute = dict()
    #     attribute['is_supported'] = True
    #     attribute['name'] = 'name'
    #     attribute['factory_definition'] = 'LazyAttribute(lambda x: faker.text(max_nb_chars=20))'
    #     attribute['type'] = 'CharField'
    #     factory['attributes'].append(attribute)
    #
    #     attribute = dict()
    #     attribute['is_supported'] = True
    #     attribute['name'] = 'notes'
    #     attribute['factory_definition'] = 'LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))'
    #     attribute['type'] = 'TextField'
    #     factory['attributes'].append(attribute)
    #
    #     attribute = dict()
    #     attribute['is_supported'] = True
    #     attribute['name'] = 'virtual'
    #     attribute['factory_definition'] = 'Iterator([True, False])'
    #     attribute['type'] = 'BooleanField'
    #     factory['attributes'].append(attribute)
    #
    #     attribute = dict()
    #     attribute['is_supported'] = True
    #     attribute['name'] = 'ip_address'
    #     attribute['factory_definition'] = 'LazyAttribute(lambda o: faker.ipv4(network=False))'
    #     attribute['type'] = 'IPAddressField'
    #     factory['attributes'].append(attribute)
    #
    #     attribute = dict()
    #     attribute['is_supported'] = False
    #     attribute['name'] = 'info'
    #     attribute['factory_definition'] = ''
    #     attribute['type'] = 'JSONField'
    #     factory['attributes'].append(attribute)
    #
    #     attribute = dict()
    #     attribute['is_supported'] = True
    #     attribute['name'] = 'created'
    #     attribute['factory_definition'] = 'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",tzinfo=timezone(settings.TIME_ZONE)))'
    #     attribute['type'] = 'DateTimeField'
    #     factory['attributes'].append(attribute)
    #     factory_data['factories'].append(factory)
    #
    #     template_name = 'factories.py.j2'
    #     writer = GenericTemplateWriter(template_name)
    #     writer.write(factory_data, self.test_write.filename)

    @temporary_file('.py', delete_on_exit=True)
    def test_write_servers(self):
        generator = FactoryBoyGenerator()
        factory_data = generator.create_template_data(settings.TEST_APP_SERVERS)
        template_name = 'factories.py.j2'
        writer = GenericTemplateWriter(template_name)
        writer.write(factory_data, self.test_write_servers.filename)
        hash = hash_file(self.test_write_servers.filename)
        self.assertEqual(hash, '5cf89c49762055625bc22ef2a09be220768edb6d')

    @temporary_file('.py', delete_on_exit=True)
    def test_write_people(self):
        generator = FactoryBoyGenerator()
        factory_template_data = generator.create_template_data(settings.TEST_APP_PEOPLE)

        template_name = 'factories.py.j2'
        writer = GenericTemplateWriter(template_name)
        writer.write(factory_template_data, self.test_write_people.filename)
        hash = hash_file(self.test_write_people.filename)
        self.assertEqual(hash, 'b2cf54a76f573b2cec349b3b11fc945487f10d68')
