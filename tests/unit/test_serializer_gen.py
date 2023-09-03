from django.conf import settings
from django.test import TestCase

from django_test_tools.app_manager import DjangoAppManager
from django_test_tools.file_utils import temporary_file
from django_test_tools.generators.serializer_gen import SerializerGenerator, AppSerializerGenerator
from tests.unit.test_model_test_gen import PythonWritingTestMixin


class TestSerializerGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = settings.TEST_APP_SERVERS
        app_manager = DjangoAppManager()
        model = app_manager.get_model(app_name, 'Server')
        model_serializer = SerializerGenerator(model)
        hash = self.write_generator_to_file(self.test_app_str.filename, model_serializer)
        if app_name == 'example.servers':
            self.assertEqual('09bef8e0953d83295b870d82f856b219d8fd68d4', hash)
        else:
            self.assertEqual(hash, '09bef8e0953d83295b870d82f856b219d8fd68d4')


class TestAppSerializerGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = settings.TEST_APP_SERVERS
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        app_serializers = AppSerializerGenerator(app)
        hash_digest = self.write_generator_to_file(self.test_app_str.filename, app_serializers)
        if app_name == 'example.servers':
            self.assertEqual('408e2da1f563da009af5da9c4c9e7ee11cc3beae', hash_digest)
        else:
            self.assertEqual(hash_digest, 'fa5509b309d47913af26c20e1800f0921a2783a8')  # FIXME Why do this?
