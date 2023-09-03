from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any, List

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
    field = FieldType.DATETIME_FIELD

    def __init__(self, start_date: str = '-1y', end_date: str = 'now', exclude: List[str] = None):
        self.start_date = start_date
        self.end_date = end_date
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.field_type == self.field and field_data.name not in self.excluded:
            field_data.required_imports = ['from django.conf import settings', 'from factory import LazyAttribute',
                                           'from faker import Factory as FakerFactory',
                                           'faker = FakerFactory.create()']
            field_data.factory_entry = (f'LazyAttribute(lambda x: faker.date_time_between('
                                        f'start_date="{self.start_date}", '
                                        f'end_date="{self.end_date}", tzinfo=timezone(settings.TIME_ZONE)))')
            return field_data
        else:
            return super().handle(field_data)


class CharFieldIdHandler(AbstractModelFieldHandler):
    """Handle id char fields for example device_id or client_number will return numbers.
    This handler will handle the field if the max_length is less than or equal to length_threshold"""
    field = FieldType.CHAR_FIELD

    def __init__(self, length_threshold: int = 32, exclude: List[str] = None):
        self.length_threshold = length_threshold
        self.digit_id_names = ['id', 'num', 'number']
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if (field_data.field_type != self.field or field_data.name in self.excluded or
            field_data.attributes.max_length > self.length_threshold):
            return super().handle(field_data)
        else:
            # Imports
            field_data.required_imports = ['import string', 'from factory import LazyAttribute',
                                           'from factory.fuzzy import FuzzyText']
            # Factory entry
            characters = 'ascii_letters'
            for din in self.digit_id_names:
                if din in field_data.name:
                    characters = 'digits'
                    break
            field_data.factory_entry = (f'LazyAttribute(lambda x: FuzzyText(length={field_data.attributes.max_length}, '
                                        f'chars=string.{characters}).fuzz())')
            return field_data


class CharFieldGenericHandler(AbstractModelFieldHandler):
    field = FieldType.CHAR_FIELD

    def __init__(self, length_threshold: int = 32, exclude: List[str] = None):
        self.length_threshold = length_threshold
        self.digit_id_names = ['id', 'num', 'number']
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.field_type != self.field or field_data.name in self.excluded:
            return super().handle(field_data)
        else:
            # Imports
            field_data.required_imports = ['import string', 'from factory import LazyAttribute',
                                           'from factory.fuzzy import FuzzyText']
            # Factory entry
            characters = 'ascii_letters'
            for din in self.digit_id_names:
                if din in field_data.name:
                    characters = 'digits'
                    break
            field_data.factory_entry = (f'LazyAttribute(lambda x: FuzzyText(length={field_data.attributes.max_length}, '
                                        f'chars=string.{characters}).fuzz())')
            return field_data
