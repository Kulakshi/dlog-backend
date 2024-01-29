from pydantic import BaseModel, Field
from enum import Enum as PydanticEnum
from typing import Dict, List, Any, Optional, TypeVar, Generic
from datetime import datetime


class DataType(PydanticEnum):
    text = "text"
    number = "number"
    boolean = "boolean"


T = TypeVar('T')


class Attribute(BaseModel, Generic[T]):
    name: str
    type: str
    value: T

class Layout(BaseModel):
    h: int = 1
    w: int = 1
    x: int = 0
    y: int = 0
    i: str = None #element id
    moved: Optional[bool] = False
    static: Optional[bool] = False


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
    hide_label: bool = False
    style: Dict[str, Any] = Field(default_factory=dict)
    layout: Optional[Layout] = None


class Form(BaseModel):
    user_id: str = None
    name: str = None
    elements: Optional[List[Element]] = None

class PersonalForm(BaseModel):
    user_id: str = None
    form_id: str = None
    hide_label: Optional[bool] = None
    layout: Optional[List[Layout]] = None

class DataEntry(BaseModel):
    user_id: str = None
    time: datetime
    form_id: str = None
    element_id: str = None
    value: T = None
