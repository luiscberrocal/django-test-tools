from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union

from django_test_tools.generators.enums import FieldTypes


class FieldHandler(ABC):
    @abstractmethod
    def set_next(self, handler: 'FieldHandler') -> 'FieldHandler':
        pass

    @abstractmethod
    def handle(self, field_payload: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AbstractFieldHandler(FieldHandler):
    _next_handler: FieldHandler = None
    field_types: List[FieldTypes] = None

    def set_next(self, handler: 'FieldHandler') -> 'FieldHandler':
        self._next_handler = handler
        return handler

    def handle(self, field_payload: Dict[str, Any]) -> Union[List[Dict[str, Any]], None]:
        if self._next_handler:
            return self._next_handler.handle(field_payload)
        return None


class CharFieldHandler(AbstractFieldHandler):
    """
    {
          "field_name": "name",
          "type": "CharField",
          "unique": true,
          "primary_key": false,
          "editable": true,
          "max_length": 20
        },
    """

    def __init__(self, numerical_identifiers: List[str] = None, code_threshold: int = 5):
        self.field_types = [FieldTypes.CHAR]
        if numerical_identifiers is None:
            self.numerical_identifiers = ['id', 'num', ]
        self.code_threshol = code_threshold

    def handle(self, field_payload: Dict[str, Any]) -> Union[List[Dict[str, Any]], None]:
        if field_payload.get('choices'):
            template = 'Iterator({choices}, getter=lambda x: x[0])'
            return template.format(**field_payload)

        if self._is_number(field_payload['field_name']):
            template = 'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.digits).fuzz())'
            return template.format(**field_payload)

        if field_payload['max_length'] > self.code_threshold:
            template = 'LazyAttribute(lambda x: faker.text(max_nb_chars={max_length}))'
            return template.format(**field_payload)
        else:
            template = 'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.ascii_letters).fuzz())'
            return template.format(**field_payload)

    def _is_number(self, field_name):
        for nv in self.numerical_identifiers:
            if nv in field_name.lower():
                return True
        return False
