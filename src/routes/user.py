
from fastapi import APIRouter, Query, Body, Depends
import pymongo
from datetime import datetime
from src.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from typing import Dict
from pydantic import BaseModel
from mongodb import get_mongo_db, MongoDB

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

router = APIRouter()

class UserEntry(BaseModel):
    user_id: int
    time: datetime
    team: str
    project: str


@router.post("/login/")
async def login(
    user: UserEntry = Body(...),
    db: MongoDB = Depends(get_mongo_db)
):
    # get element by id -> get type -> according to type validate value and enter data
    return {"message": "Instance created successfully"}


