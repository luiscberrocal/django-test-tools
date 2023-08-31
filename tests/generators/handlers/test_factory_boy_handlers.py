from unittest import mock

from django.test import SimpleTestCase

from django_test_tools.generators.enums import FieldType
from django_test_tools.generators.handlers.factory_boy_handlers import DateTimeFieldHandler, TextFieldHandler, \
    IntegerFieldHandler
from django_test_tools.generators.models import FieldInfo


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
        field_info = FieldInfo(type=FieldType.TEXT, field_name="description")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


# Test for IntegerFieldHandler
class TestIntegerFieldHandler(SimpleTestCase):

    def setUp(self):
        self.handler = IntegerFieldHandler()

    def test_handle_integer_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, [
            'from faker import Factory as FakerFactory',
            'faker = FakerFactory.create()'
        ])
        self.assertIn("faker.random_int", result.factory_entry)

    def test_handle_non_integer_field(self):
        field_info = FieldInfo(type=FieldType.TEXT, field_name="description")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


# Test for TextFieldHandler
class TestTextFieldHandler(SimpleTestCase):

    def setUp(self):
        self.handler = TextFieldHandler()

    def test_handle_text_field(self):
        field_info = FieldInfo(type=FieldType.TEXT, field_name="description")
        result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, [
            'from faker import Factory as FakerFactory',
            'faker = FakerFactory.create()'
        ])
        self.assertIn("faker.paragraph", result.factory_entry)

    def test_handle_non_text_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)
