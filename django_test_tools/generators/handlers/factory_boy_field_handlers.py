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
    def handle(self, field_data: FieldInfo) -> Dict[str, Any] | None:
        pass


class AbstractModelFieldHandler(ModelFieldHandler):
    _next_handler: ModelFieldHandler = None
    field = None

    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        self._next_handler = handler
        return handler

    def handle(self, field_data: FieldInfo) -> Dict[str, Any] | None:
        if self._next_handler:
            return self._next_handler.handle(field_data)
        return None


class DateTimeFieldHandler(AbstractModelFieldHandler):
    field = FieldType.DATETIME_FIELD

    def handle(self, field_data: FieldInfo ) -> Dict[str, Any] | None:
        if field_data.field_type == self.field:
            field_data['factory_field'] = 'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", ' \
                                          'end_date="now", tzinfo=timezone(settings.TIME_ZONE)))'
            return field_data
        else:
            return super().handle(field_data)
