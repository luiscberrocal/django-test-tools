from abc import ABC, abstractmethod
from typing import List

from django_test_tools.generators.enums import FieldType
from django_test_tools.generators.models import FieldInfo


class ModelFieldHandler(ABC):
    @abstractmethod
    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        pass

    @abstractmethod
    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        pass


class AbstractModelFieldHandler(ModelFieldHandler):
    _next_handler: ModelFieldHandler = None
    field = None

    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        self._next_handler = handler
        return handler

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if self._next_handler:
            return self._next_handler.handle(field_data)
        return None


class DateTimeFieldHandler(AbstractModelFieldHandler):
    field = FieldType.DATETIME

    def __init__(self, start_date: str = '-1y', end_date: str = 'now', exclude: List[str] = None):
        self.start_date = start_date
        self.end_date = end_date
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type == self.field and field_data.field_name not in self.excluded:
            field_data.required_imports = ['from django.conf import settings', 'from factory import LazyAttribute',
                                           'from faker import Factory as FakerFactory',
                                           'faker = FakerFactory.create()']
            field_data.factory_entry = (f'LazyAttribute(lambda x: faker.date_time_between('
                                        f'start_date="{self.start_date}", '
                                        f'end_date="{self.end_date}", tzinfo=timezone(settings.TIME_ZONE)))')
            return field_data
        else:
            return super().handle(field_data)


class DateFieldHandler(AbstractModelFieldHandler):
    field = FieldType.DATE

    def __init__(self, start_date: str = '-1y', end_date: str = 'now', exclude: List[str] = None):
        self.start_date = start_date
        self.end_date = end_date
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type == self.field and field_data.field_name not in self.excluded:
            field_data.required_imports = ['from django.conf import settings', 'from factory import LazyAttribute',
                                           'from faker import Factory as FakerFactory',
                                           'faker = FakerFactory.create()']
            field_data.factory_entry = (f'LazyAttribute(lambda x: faker.date_between('
                                        f'start_date="{self.start_date}", '
                                        f'end_date="{self.end_date}", tzinfo=timezone(settings.TIME_ZONE)))')
            return field_data
        else:
            return super().handle(field_data)


class CharFieldIdHandler(AbstractModelFieldHandler):
    """Handle id char fields for example device_id or client_number will return numbers.
    This handler will handle the field if the max_length is less than or equal to length_threshold"""
    field = FieldType.CHAR

    def __init__(self, length_threshold: int = 32, exclude: List[str] = None):
        self.length_threshold = length_threshold
        self.digit_id_names = ['id', 'num', 'number']
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if (field_data.type != self.field or field_data.field_name in self.excluded or
            field_data.max_length > self.length_threshold):
            return super().handle(field_data)
        else:
            # Imports
            field_data.required_imports = ['import string', 'from factory import LazyAttribute',
                                           'from factory.fuzzy import FuzzyText']
            # Factory entry
            characters = 'ascii_letters'
            for din in self.digit_id_names:
                if din in field_data.field_name:
                    characters = 'digits'
                    break
            field_data.factory_entry = (f'LazyAttribute(lambda x: FuzzyText(length={field_data.max_length}, '
                                        f'chars=string.{characters}).fuzz())')
            return field_data


class CharFieldGenericHandler(AbstractModelFieldHandler):
    field = FieldType.CHAR

    def __init__(self, length_threshold: int = 32, exclude: List[str] = None):
        self.length_threshold = length_threshold
        self.digit_id_names = ['id', 'num', 'number']
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type != self.field or field_data.field_name in self.excluded:
            return super().handle(field_data)
        else:
            if field_data.max_length > self.length_threshold:
                field_data.required_imports = ['from factory import LazyAttribute',
                                               'from faker import Factory as FakerFactory',
                                               'faker = FakerFactory.create()']
                field_data.factory_entry = (f'LazyAttribute(lambda x: faker.text(max_nb_chars='
                                            f'{field_data.max_length}))')

            else:
                # Imports
                field_data.required_imports = ['import string', 'from factory import LazyAttribute',
                                               'from factory.fuzzy import FuzzyText']
                # Factory entry
                field_data.factory_entry = (f'LazyAttribute(lambda x: '
                                            f'FuzzyText(length={field_data.max_length}, '
                                            f'chars=string.ascii_letters).fuzz())')
            return field_data


class DecimalFieldHandler(AbstractModelFieldHandler):
    field = FieldType.DECIMAL

    def __init__(self, is_positive: bool = True, exclude: List[str] = None):
        self.is_positive = is_positive
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type != self.field or field_data.field_name in self.excluded:
            return super().handle(field_data)
        else:
            field_data.required_imports = ['from factory import LazyAttribute',
                                           'from faker import Factory as FakerFactory',
                                           'faker = FakerFactory.create()']
            left_digits = field_data.max_digits - field_data.decimal_places
            template = f'LazyAttribute(lambda x: faker.pydecimal(left_digits={left_digits}, ' \
                       f'right_digits={field_data.decimal_places}, positive={self.is_positive}))'
            field_data.factory_entry = template
            return field_data


class ForeignKeyFieldHandler(AbstractModelFieldHandler):
    field = FieldType.FOREIGNKEY

    def __init__(self, exclude: List[str] = None):
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type != self.field or field_data.field_name in self.excluded:
            return super().handle(field_data)
        else:
            field_data.required_imports = ['from factory import SubFactory']
            template = f'SubFactory({field_data.remote_field}Factory)'
            field_data.factory_entry = template
            return field_data


class IntegerFieldHandler(AbstractModelFieldHandler):
    field = FieldType.INTEGER

    def __init__(self, min_value: int = 0, max_value: int = 100_000, exclude: List[str] = None):
        self.min_value = min_value
        self.max_value = max_value
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type != self.field or field_data.field_name in self.excluded:
            return super().handle(field_data)
        else:
            field_data.required_imports = ['from faker import Factory as FakerFactory',
                                           'faker = FakerFactory.create()']
            template = f'LazyAttribute(lambda x: faker.random_int(min={self.min_value}, max={self.max_value})'
            field_data.factory_entry = template
            return field_data


class TextFieldHandler(AbstractModelFieldHandler):
    field = FieldType.TEXT

    def __init__(self, sentences: int = 3, exclude: List[str] = None):
        self.sentences = sentences
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.type != self.field or field_data.field_name in self.excluded:
            return super().handle(field_data)
        else:
            field_data.required_imports = ['from faker import Factory as FakerFactory',
                                           'faker = FakerFactory.create()']
            template = (f'LazyAttribute(lambda x: faker.paragraph(nb_sentences={self.sentences}, '
                        f'variable_nb_sentences=True))')
            field_data.factory_entry = template
            return field_data
