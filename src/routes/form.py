from fastapi import APIRouter, Query, Body, Depends
from mongodb import get_mongo_db, MongoDB
from src.models.commons import ApiResponse
from src.models.elements import Element, DataEntry, PersonalElement
from bson import ObjectId
from fastapi import HTTPException, status

router = APIRouter()


@router.get("/all/")
async def get_all_forms(
        db: MongoDB = Depends(get_mongo_db)
):
    forms = list(db.forms.find())
    for document in forms:
        if '_id' in document and isinstance(document['_id'], ObjectId):
            document['_id'] = str(document['_id'])
    return ApiResponse(code=200, response={"forms": forms})


@router.get("/{user_id}/{form_id}/")
async def get_all_forms(
        form_id: str,
        user_id: str,
        db: MongoDB = Depends(get_mongo_db)
):
    form = db.forms.find_one({"_id": ObjectId(form_id)})

    if '_id' in form and isinstance(form['_id'], ObjectId):
        form['_id'] = str(form['_id'])

    personalElements = db.personalElements.find({"user_id": user_id, "form_id": form_id})
    elementIdToElem = {elem['element_id'] : elem for elem in list(personalElements)}
    for element in form['elements']:
        if element['element_id'] in elementIdToElem.keys():
            element['customLabel'] = (elementIdToElem[element['element_id']])['customLabel']

    return ApiResponse(code=200, response={"form": form})


@router.post("/personalize/")
async def personalize_element(
        entry: PersonalElement = Body(...),
        db: MongoDB = Depends(get_mongo_db)
):
    element = db.personalElements.find_one({"user_id": entry.user_id, "element_id":entry.element_id})
    result = None
    if element:
        result = db.personalElements.update_one({"user_id": entry.user_id, "element_id":entry.element_id}, {"$set": entry.dict()})
        if result.modified_count > 0 : return ApiResponse(code=200, response={"message": "Instance updated successfully"})
    else:
        result = db.personalElements.insert_one(entry.dict())
        if result.inserted_id: return ApiResponse(code=200, response={"message": "Instance added successfully"})

    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert entry into the database")







@router.post("/add-entry/")
async def add_data_entry(
        entry: DataEntry = Body(...),
        db: MongoDB = Depends(get_mongo_db)
):

    # data type validation
    # element_type = entry.element_type
    # # Validate the value based on the element type
    # if element_type == "number":
    #     if not isinstance(entry.value, int) or not isinstance(entry.value, float):
    #         raise HTTPException(status_code=422, detail="Invalid value type for integer element")
    #
    # elif element_type == "string":
    #     if not isinstance(entry.value, str):
    #         raise HTTPException(status_code=422, detail="Invalid value type for string element")

    result = db.entries.insert_one({
        "user_id": entry.user_id,
        "time": entry.time,
        "form_id": entry.form_id,
        "element_id": entry.element_id,
        "value": entry.value
    })

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert entry into the database")

    return ApiResponse(code=200, response={"message": "Instance created successfully"})
