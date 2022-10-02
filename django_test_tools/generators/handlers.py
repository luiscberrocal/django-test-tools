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

    def handle(self, payment_payload: Dict[str, Any]) -> Union[List[Dict[str, Any]], None]:
        if self._next_handler:
            return self._next_handler.handle(payment_payload)
        return None
