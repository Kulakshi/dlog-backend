from pydantic import BaseModel, Field
from enum import Enum as PydanticEnum
from typing import Dict, List, Any, Optional, TypeVar, Generic
from datetime import datetime


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

class Element(BaseModel):
    element_id: Optional[str] = None
    element_type: str = None
    attributes: List[Attribute] = []
    label: Optional[str] = None
    style: Dict[str, Any] = Field(default_factory=dict)


class Form(BaseModel):
    user_id: str = None
    name: str = None
    elements: Optional[List[Element]] = None

class DataEntry(BaseModel):
    user_id: str = None
    time: datetime
    form_id: str = None
    element_id: str = None
    value: T = None
