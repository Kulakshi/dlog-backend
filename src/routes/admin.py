from fastapi import APIRouter, Query, Body, Depends
from fastapi import HTTPException, status
from mongodb import get_mongo_db, MongoDB
from src.models.elements import Element, Form
from src.models.commons import ApiResponse
from bson import ObjectId

router = APIRouter()


@router.get("/{user_id}/forms/")
async def get_forms(
        user_id: str,
        db: MongoDB = Depends(get_mongo_db)
):
    forms = list(db.forms.find({"user_id": user_id}))
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
    result = db.forms.insert_one(new_form)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert form into the database")

    form = db.forms.find_one({"_id": ObjectId(result.inserted_id)})
    for (i, elem) in enumerate(form['elements']):
        elem['element_id'] = str(form['_id']) + "_" + str(i + 1)
    db.forms.update_one({"_id": ObjectId(result.inserted_id)}, {"$set": form})

    print(form)
    form['_id'] = str(form['_id'])

    return ApiResponse(code=200, response={"message": "Form created successfully",
                                           "form": form})


@router.get("/get-form-structures/")
async def get_form_structures():
    return ApiResponse(code=200, response={"form": Form().dict(), "element": Element().dict()})
