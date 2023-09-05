from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from django_test_tools.generators.enums import FieldType


class FieldInfo(BaseModel):
    field_name: str
    type: FieldType
    primary_key: bool = Field(default=False, description='Is primary key?')
    editable: bool = Field(default=True, description='Is editable?')
    factory_entry = Optional[str]
    required_imports: Optional[List[str]]
    max_length: Optional[int] = Field(description='Maximum length of field. Used by CharField.')
    choice_type: Optional[str]
    choices: Optional[List[List]]
    max_digits: Optional[int] = Field(description='Maximum number of digits. Used by DecimalField')
    decimal_places: Optional[int] = Field(description='Decimal places. Used by DecimalField')
    remote_field: Optional[str] = Field(description='Name of the foreign model. Used by ForeignKey')

    class Config:
        arbitrary_types_allowed = True


class ModelInfo(BaseModel):
    model_name: str
    # package_name: str
    fields: List[FieldInfo]


class AppInfo(BaseModel):
    app_name: str
    package_name: str
    models: Dict[str, Any]
