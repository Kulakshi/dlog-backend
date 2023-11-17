
from fastapi import APIRouter, Query
import pymongo
from src.models import elements
from src.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

router = APIRouter()
@router.post("/create_element/")
async def create_instance(element: elements.Element):
    instance_data = element.dict()
    collection.insert_one(instance_data)
    return {"message": "Instance created successfully"}

@router.get("/get_instances/")
async def get_instances():
    instances = list(collection.find())
    return instances

@router.get("/get_instances/")
async def get_instances(type_of_element: str = Query(None, description="Filter by type of element")):
    query_params = {}
    if type_of_element:
        query_params["typeOfElement"] = type_of_element

    instances = list(collection.find(query_params))
    return instances

def generate_dummy_data():
    return [
        {"id": 1, "label": "Dummy Label 1", "typeOfElement": "dummyType"},
        {"id": 2, "label": "Dummy Label 2", "typeOfElement": "dummyType"},
        # Add more dummy data as needed
    ]

@router.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}
