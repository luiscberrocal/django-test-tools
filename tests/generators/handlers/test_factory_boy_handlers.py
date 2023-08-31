from unittest import mock

from django.test import SimpleTestCase

from django_test_tools.generators.enums import FieldType
from django_test_tools.generators.handlers.factory_boy_handlers import DateTimeFieldHandler
from django_test_tools.generators.models import FieldInfo


# Mocking FieldInfo class as it seems to be an external dependency not provided.
class MockFieldInfo:
    def __init__(self, type, field_name):
        self.type = type
        self.field_name = field_name
        self.required_imports = []
        self.factory_entry = None


# Mocking FieldType enum as it seems to be an external dependency not provided.
class MockFieldType:
    DATETIME = "DATETIME"
    FOREIGN_KEY = "FOREIGN_KEY"
    INTEGER = "INTEGER"
    TEXT = "TEXT"


# Mocked settings.TIME_ZONE for the DateTimeFieldHandler
class MockSettings:
    TIME_ZONE = "UTC"


# Test for DateTimeFieldHandler
class TestDateTimeFieldHandler(SimpleTestCase):

    def setUp(self):
        self.handler = DateTimeFieldHandler()

    def test_handle_datetime_field(self):
        field_info = FieldInfo(type=FieldType.DATETIME, field_name="created_at")

        with mock.patch("django.conf.settings", MockSettings):
            result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, [
            'from django.conf import settings',
            'from factory import LazyAttribute',
            'from faker import Factory as FakerFactory',
            'faker = FakerFactory.create()'
        ])
        self.assertIn("faker.date_time_between", result.factory_entry)

    def test_handle_non_datetime_field(self):
        field_info = MockFieldInfo(MockFieldType.TEXT, "description")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)
