from pydantic import BaseModel, Field
from enum import Enum as PydanticEnum
from typing import Dict, List, Any, Optional, TypeVar, Generic


class DataType(PydanticEnum):
    text = "text"
    number = "number"


T = TypeVar('T')


class Attribute(BaseModel, Generic[T]):
    name: str
    type: str
    value: T


class ElementType(BaseModel):
    name: str
    attributes: List[Attribute] = []
    style: Optional[Dict[str, Any]]
    actions: dict = Optional[Dict[str, Any]]


class ElementInstance(BaseModel):
    element_type_id: str = None
    attributes: List[Attribute] = []
    label: Optional[str] = None
    customLabel: Optional[str] = None
    hideLabel: bool = True
    style: Dict[str, Any] = Field(default_factory=dict)


class Form(BaseModel):
    user_id: str = None
    name: str = None
    elements: Optional[List[ElementInstance]] = None
