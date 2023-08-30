from typing import Optional, List

from pydantic import BaseModel, Field

from django_test_tools.generators.enums import FieldType


class FieldAttributes(BaseModel):
    max_length: Optional[int] = Field(description='Maximum length of field. Used by CharField.')
    max_digits: Optional[int] = Field(description='Maximum number of digits. Used by DecimalField')
    decimal_places: Optional[int] = Field(description='Decimal places. Used by DecimalField')
    positive: Optional[bool] = Field(description='Are values only positive? Used by DecimalField')
    model_name: Optional[str] = Field(description='Name of the foreign model. Used by ForeignKey')


class FieldInfo(BaseModel):
    name: str
    field_type: FieldType
    factory_entry = Optional[str]
    attributes: Optional[FieldAttributes]
    required_imports: Optional[List[str]]


class ModelInfo(BaseModel):
    name: str
    fields: List[FieldInfo]
