from typing import Optional

from pydantic import BaseModel

from django_test_tools.generators.enums import FieldType


class FieldInfo(BaseModel):
    name: str
    field_type: FieldType
    factory_entry = Optional[str]


class ModelInfo(BaseModel):
    name: str
