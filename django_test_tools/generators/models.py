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
    field_name: str
    type: FieldType
    primary_key: bool
    editable: bool
    factory_entry = Optional[str]
    # attributes: Optional[FieldAttributes]
    required_imports: Optional[List[str]]
    max_length: Optional[int] = Field(description='Maximum length of field. Used by CharField.')
    choice_type: Optional[str]
    choices: Optional[List[List]]
    max_digits: Optional[int] = Field(description='Maximum number of digits. Used by DecimalField')
    decimal_places: Optional[int] = Field(description='Decimal places. Used by DecimalField')
    remote_field: Optional[str] = Field(description='Name of the foreign model. Used by ForeignKey')


class ModelInfo(BaseModel):
    model_name: str
    fields: List[FieldInfo]
