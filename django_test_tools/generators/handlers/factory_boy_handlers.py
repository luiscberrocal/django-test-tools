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

    def __init__(self, exclude: List[str] = None):
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.field_type == self.field and field_data.name not in self.excluded:
            field_data.factory_entry = 'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", ' \
                                       'end_date="now", tzinfo=timezone(settings.TIME_ZONE)))'
            return field_data
        else:
            return super().handle(field_data)


class CharFieldIdHandler(AbstractModelFieldHandler):
    field = FieldType.CHAR_FIELD

    def __init__(self, exclude: List[str] = None):
        self.digit_id_names = ['id', 'num', 'number']
        if exclude is None:
            self.excluded = []
        else:
            self.excluded = exclude

    def handle(self, field_data: FieldInfo) -> FieldInfo | None:
        if field_data.field_type == self.field and field_data.name not in self.excluded:
            characters = 'ascii_letters'
            for din in self.digit_id_names:
                if din in field_data.name:
                    characters = 'digits'
                    break
            field_data.factory_entry = (f'LazyAttribute(lambda x: FuzzyText(length={field_data.attributes.max_length}, '
                                        f'chars=string.{characters}).fuzz())')
            return field_data
        else:
            return super().handle(field_data)
