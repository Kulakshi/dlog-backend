from fastapi import APIRouter, Query, Body, Depends
from fastapi import HTTPException, status
from mongodb import get_mongo_db, MongoDB
from src.models.elements import ElementInstance, Form
from src.models.commons import ApiResponse
from bson import ObjectId

router = APIRouter()


@router.get("/{user_id}/forms/")
async def get_forms(
        user_id: str,
        db: MongoDB = Depends(get_mongo_db)
):
    forms = list(db.forms.find({"user_id": user_id}))
    print(forms)
    for document in forms:
        if '_id' in document and isinstance(document['_id'], ObjectId):
            document['_id'] = str(document['_id'])
    return ApiResponse(code=200, response={"forms": forms})


@router.post("/create-form/")
async def create_form(
        entry: Form = Body(...),
        db: MongoDB = Depends(get_mongo_db)
):
    existing_form = db.forms.find_one({"user_id": entry.user_id, "name": entry.name})
    if existing_form:
        raise HTTPException(status_code=404, detail="Form already exists")

    new_form = entry.dict()
    form = db.forms.insert_one(new_form)

    if not form.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert form into the database")

    return ApiResponse(code=200, response={"message": "Form created successfully",
                                           "form": {"form_id": str(form.inserted_id), "name": entry.name}})


@router.get("/get-form-structures/")
async def get_form_structures():
    return ApiResponse(code=200, response={"form": Form().dict(), "element": ElementInstance().dict()})


@router.post("/add-entry/")
async def add_entry(
        entry: ElementInstance = Body(...),
        db: MongoDB = Depends(get_mongo_db)
):
    # get element by id -> get type -> according to type validate value and enter data

    # Get element by ID from MongoDB
    element = db.elements.find_one({"_id": entry.element_id})

    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    element_type = element.get("type")

    # Validate the value based on the element type
    if element_type == "integer":
        if not isinstance(entry.value, int):
            raise HTTPException(status_code=422, detail="Invalid value type for integer element")

    elif element_type == "string":
        if not isinstance(entry.value, str):
            raise HTTPException(status_code=422, detail="Invalid value type for string element")

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
