
from fastapi import APIRouter, Query, HTTPException, Depends, Body
from src.models import elements
from mongodb import get_mongo_db, MongoDB
from src.models.commons import ApiResponse
from pydantic import ValidationError


router = APIRouter()
@router.post("/create/")
async def create_instance(
        element: elements.ElementInstance = Body(...),
        db: MongoDB = Depends(get_mongo_db)):
    instance_data = element.dict()
    db.elements.insert_one(instance_data)
    return ApiResponse(code=200, response={"message": "Instance created successfully"})

@router.get("/get_instances/")
async def get_instances(db: MongoDB = Depends(get_mongo_db)):
    instances = list(db.elements.find())
    return instances

@router.get("/get_instances/")
async def get_instances(type_of_element: str = Query(None, description="Filter by type of element"), db: MongoDB = Depends(get_mongo_db)):
    query_params = {}
    if type_of_element:
        query_params["typeOfElement"] = type_of_element

    instances = list(db.elements.find(query_params))
    return instances

@router.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None, db: MongoDB = Depends(get_mongo_db)):
    return {"item_id": item_id, "query_param": query_param}
