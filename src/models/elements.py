from pydantic import BaseModel, Field
from enum import Enum as PydanticEnum
from typing import Dict, Any

class ElementType(PydanticEnum):
    button = "button"
    slider = "slider"

class AdditionalAttributes(BaseModel):
    custom_attributes: dict = Field(default_factory=dict)

class Element(BaseModel):
    id: int
    label: str
    customLabel: str
    hideLabel: bool
    style: Dict[str, Any]
    typeOfElement: ElementType
    additionalAttributes: AdditionalAttributes
