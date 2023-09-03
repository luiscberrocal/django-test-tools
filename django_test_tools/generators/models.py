from typing import Optional, List

from pydantic import BaseModel

from django_test_tools.generators.enums import FieldType

class FieldAttributes(BaseModel):
    max_length: Optional[int]


class FieldInfo(BaseModel):
    name: str
    field_type: FieldType
    factory_entry = Optional[str]
    attributes: FieldAttributes

class ModelInfo(BaseModel):
    name: str
    fields: List[FieldInfo]
