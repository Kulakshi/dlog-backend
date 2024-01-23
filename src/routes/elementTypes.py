from fastapi import APIRouter, Query, Body, Depends
from fastapi import HTTPException
from datetime import datetime
from mongodb import get_mongo_db, MongoDB
from src.models.elements import Attribute, ElementType, Element
from src.data.elements import default_elements
from src.models.commons import ApiResponse
from bson.json_util import dumps

router = APIRouter()


# Function to insert default elements
def insert_default_elements():
    db = MongoDB().get_database()
    for default_element in default_elements:
        existing_element = db.elementTypes.find_one({"name": default_element.name})
        if not existing_element:
            db.elementTypes.insert_one(default_element.dict())
        print("Added default elements")


# Event to execute on startup
@router.on_event("startup")
def on_startup():
    insert_default_elements()


@router.get("/get-elements", response_model=ApiResponse)
async def get_available_types(db: MongoDB = Depends(get_mongo_db)):
    types_from_db = db.elementTypes.distinct("name")
    return ApiResponse(code=200, response={"types": types_from_db})


@router.get("/{type_name}")
async def get_instance(type_name: str, db: MongoDB = Depends(get_mongo_db)):
    type_data = db.elementTypes.find_one({"name": type_name})
    if type_data:
        attributes = [
            Attribute(**attr) for attr in type_data.get('attributes', [])
        ]
        element_instance = Element(
            element_type=str(type_data['name']),
            attributes=attributes
        )
        return ApiResponse(code=200, response={"type": element_instance})
    raise HTTPException(status_code=404, detail="Type not found")


@router.post("/create", response_model=dict)
async def create_custom_type(
        element: ElementType,
        db: MongoDB = Depends(get_mongo_db)
):
    existing_element = db.elementTypes.find_one({"name": element.name})
    if existing_element:
        raise HTTPException(status_code=400, detail="Element with the same name already exists")

    new_element = ElementType(
        id=str(datetime.utcnow().timestamp()),
        name=element.name,
        style=element.style,
        attributes=element.attributes,
        actions=element.actions,
    )
    db.elementTypes.insert_one(new_element)
    return new_element
