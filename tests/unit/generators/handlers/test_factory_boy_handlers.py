from unittest import mock

from django.test import SimpleTestCase

from django_test_tools.generators.enums import FieldType
from django_test_tools.generators.handlers.factory_boy_handlers import DateTimeFieldHandler, TextFieldHandler, \
    IntegerFieldHandler, DateFieldHandler, CharFieldIdHandler, CharFieldGenericHandler, DecimalFieldHandler, \
    EmailFieldGenericHandler, ForeignKeyFieldHandler, CHAINED_HANDLERS
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


class TestDateFieldHandler(SimpleTestCase):

    def setUp(self):
        self.handler = DateFieldHandler()

    def test_handle_date_field(self):
        field_info = FieldInfo(type=FieldType.DATE, field_name="paid_on")

        with mock.patch("django.conf.settings", MockSettings):
            result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, [
            'from django.conf import settings',
            'from factory import LazyAttribute',
            'from faker import Factory as FakerFactory',
            'faker = FakerFactory.create()'
        ])
        self.assertIn("faker.date_between", result.factory_entry)

    def test_handle_non_date_field(self):
        field_info = FieldInfo(type=FieldType.TEXT, field_name="description")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


class TestCharFieldIdHandler(SimpleTestCase):

    def setUp(self):
        self.handler = CharFieldIdHandler()

    def test_handle_char_id_field(self):
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device_id", max_length=32)
        result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, ['import string', 'from factory import LazyAttribute',
                                                   'from factory.fuzzy import FuzzyText'])
        expected = (f'LazyAttribute(lambda x: FuzzyText(length={field_info.max_length}, '
                    f'chars=string.digits).fuzz())')
        self.assertEqual(result.factory_entry, expected)

    def test_handle_char_id_ascii(self):
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device", max_length=16)
        result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, ['import string', 'from factory import LazyAttribute',
                                                   'from factory.fuzzy import FuzzyText'])
        expected = (f'LazyAttribute(lambda x: FuzzyText(length={field_info.max_length}, '
                    f'chars=string.ascii_letters).fuzz())')
        self.assertEqual(result.factory_entry, expected)

    def test_handle_greater_than_threshold(self):
        handler = CharFieldIdHandler(length_threshold=16)
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device_id", max_length=32)
        result = handler.handle(field_info)
        self.assertIsNone(result)

    def test_handle_non_char_id_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


class TestCharFieldGenericHandler(SimpleTestCase):

    def setUp(self):
        self.handler = CharFieldGenericHandler()

    def test_handle_char_generic_field(self):
        max_len = self.handler.length_threshold
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device", max_length=max_len)
        result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, ['import string', 'from factory import LazyAttribute',
                                                   'from factory.fuzzy import FuzzyText'])
        expected = (f'LazyAttribute(lambda x: '
                    f'FuzzyText(length={max_len}, '
                    f'chars=string.ascii_letters).fuzz())')
        self.assertEqual(result.factory_entry, expected)

    def test_handle_char_generic_field_past_threshold(self):
        max_len = self.handler.length_threshold + 1
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device", max_length=max_len)
        result = self.handler.handle(field_info)

        self.assertEqual(result.required_imports, ['from factory import LazyAttribute',
                                                   'from faker import Factory as FakerFactory',
                                                   'faker = FakerFactory.create()'])
        expected = (f'LazyAttribute(lambda x: faker.text(max_nb_chars='
                    f'{max_len}))')
        self.assertEqual(result.factory_entry, expected)

    def test_handle_non_char_id_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


class TestDecimalFieldHandler(SimpleTestCase):

    def setUp(self):
        self.handler = DecimalFieldHandler()

    def test_handle_char_decimal_field(self):
        m_digits = 10
        decimals = 2
        is_positive = True
        field_info = FieldInfo(type=FieldType.DECIMAL, field_name="amount", max_digits=m_digits,
                               decimal_places=decimals, positive=is_positive)
        result = self.handler.handle(field_info)

        expected_imports = ['from factory import LazyAttribute',
                            'from faker import Factory as FakerFactory',
                            'faker = FakerFactory.create()']
        left_digits = m_digits - decimals
        expected = f'LazyAttribute(lambda x: faker.pydecimal(left_digits={left_digits}, ' \
                   f'right_digits={decimals}, positive=True))'
        self.assertEqual(result.required_imports, expected_imports)
        self.assertEqual(result.factory_entry, expected)

    def test_handle_non_decimal_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


class TestEmailFieldGenericHandler(SimpleTestCase):

    def setUp(self):
        self.handler = EmailFieldGenericHandler()

    def test_handle_email_field(self):
        field_info = FieldInfo(type=FieldType.EMAIL, field_name="email")
        result = self.handler.handle(field_info)

        expected_required_imports = ['from factory import LazyAttribute',
                                     'from faker import Factory as FakerFactory',
                                     'faker = FakerFactory.create()']
        expected_factory_entry = 'LazyAttribute(lambda x: faker.free_email())'

        self.assertEqual(result.required_imports, expected_required_imports)
        self.assertEqual(result.factory_entry, expected_factory_entry)

    def test_handle_non_email_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


class TestForeignKeyFieldGenericHandler(SimpleTestCase):

    def setUp(self):
        self.handler = ForeignKeyFieldHandler()

    def test_handle_foreign_key_field(self):
        field = "customer"
        remote_field = 'Customer'
        field_info = FieldInfo(type=FieldType.FOREIGN_KEY, field_name=field, remote_field=remote_field)
        result = self.handler.handle(field_info)

        expected_required_imports = ['from factory import SubFactory']
        expected_factory_entry = f'SubFactory({remote_field}Factory)'

        self.assertEqual(result.required_imports, expected_required_imports)
        self.assertEqual(result.factory_entry, expected_factory_entry)

    def test_handle_non_foreign_key_field(self):
        field_info = FieldInfo(type=FieldType.INTEGER, field_name="age")
        result = self.handler.handle(field_info)
        self.assertIsNone(result)


class TestChainedHandlers(SimpleTestCase):

    def test_handle_char_generic_field(self):
        max_len = 26
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device", max_length=max_len)
        result = CHAINED_HANDLERS.handle(field_info)

        self.assertEqual(result.required_imports, ['import string', 'from factory import LazyAttribute',
                                                   'from factory.fuzzy import FuzzyText'])
        expected = (f'LazyAttribute(lambda x: '
                    f'FuzzyText(length={max_len}, '
                    f'chars=string.ascii_letters).fuzz())')
        self.assertEqual(result.factory_entry, expected)

    def test_handle_foreign_key_field(self):
        field = "client"
        remote_field = 'Client'
        field_info = FieldInfo(type=FieldType.FOREIGN_KEY, field_name=field, remote_field=remote_field)
        result = CHAINED_HANDLERS.handle(field_info)

        expected_required_imports = ['from factory import SubFactory']
        expected_factory_entry = f'SubFactory({remote_field}Factory)'

        self.assertEqual(result.required_imports, expected_required_imports)
        self.assertEqual(result.factory_entry, expected_factory_entry)

    def test_handle_email_field(self):
        field_info = FieldInfo(type=FieldType.EMAIL, field_name="email")
        result = CHAINED_HANDLERS.handle(field_info)

        expected_required_imports = ['from factory import LazyAttribute',
                                     'from faker import Factory as FakerFactory',
                                     'faker = FakerFactory.create()']
        expected_factory_entry = 'LazyAttribute(lambda x: faker.free_email())'

        self.assertEqual(result.required_imports, expected_required_imports)
        self.assertEqual(result.factory_entry, expected_factory_entry)

    def test_handle_char_decimal_field(self):
        m_digits = 10
        decimals = 2
        is_positive = True
        field_info = FieldInfo(type=FieldType.DECIMAL, field_name="amount", max_digits=m_digits,
                               decimal_places=decimals, positive=is_positive)
        result = CHAINED_HANDLERS.handle(field_info)

        expected_imports = ['from factory import LazyAttribute',
                            'from faker import Factory as FakerFactory',
                            'faker = FakerFactory.create()']
        left_digits = m_digits - decimals
        expected = f'LazyAttribute(lambda x: faker.pydecimal(left_digits={left_digits}, ' \
                   f'right_digits={decimals}, positive=True))'
        self.assertEqual(result.required_imports, expected_imports)
        self.assertEqual(result.factory_entry, expected)
    def test_handle_char_generic_field(self):
        max_len = 32
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device", max_length=max_len)
        result = CHAINED_HANDLERS.handle(field_info)

        self.assertEqual(result.required_imports, ['import string', 'from factory import LazyAttribute',
                                                   'from factory.fuzzy import FuzzyText'])
        expected = (f'LazyAttribute(lambda x: '
                    f'FuzzyText(length={max_len}, '
                    f'chars=string.ascii_letters).fuzz())')
        self.assertEqual(result.factory_entry, expected)

    def test_handle_char_generic_field_past_threshold(self):
        max_len = 33
        field_info = FieldInfo(type=FieldType.CHAR, field_name="device", max_length=max_len)
        result = CHAINED_HANDLERS.handle(field_info)

        self.assertEqual(result.required_imports, ['from factory import LazyAttribute',
                                                   'from faker import Factory as FakerFactory',
                                                   'faker = FakerFactory.create()'])
        expected = (f'LazyAttribute(lambda x: faker.text(max_nb_chars='
                    f'{max_len}))')
        self.assertEqual(result.factory_entry, expected)
