
from fastapi import APIRouter, Query, Body, Depends
import pymongo
from datetime import datetime
from src.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from typing import Dict, Optional
from pydantic import BaseModel
from mongodb import get_mongo_db, MongoDB

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

router = APIRouter()

class ElementEntry(BaseModel):
    user_id: int
    time: datetime
    form_id: int
    element_id: int
    value: Optional[Dict] = None


@router.post("/add-entry/")
async def add_entry(
    entry: ElementEntry = Body(...),
    db: MongoDB = Depends(get_mongo_db)
):
    # get element by id -> get type -> according to type validate value and enter data
    return {"message": "Instance created successfully"}


