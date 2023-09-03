from pydantic import BaseModel


class FieldInfo(BaseModel):
    name: str


class ModelInfo(BaseModel):
    name: str
