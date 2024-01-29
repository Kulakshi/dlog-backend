from fastapi import APIRouter, Request, Body, Depends
from mongodb import get_mongo_db, MongoDB
from src.models.commons import ApiResponse
from src.models.elements import Element, DataEntry, PersonalForm
from bson import ObjectId
from fastapi import HTTPException, status
import asyncio

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


@router.get("/{user_role}/{user_id}/{form_id}/")
async def get_all_forms(
        user_role: str,
        form_id: str,
        user_id: str,
        db: MongoDB = Depends(get_mongo_db)
):
    form = db.forms.find_one({"_id": ObjectId(form_id)})

    if '_id' in form and isinstance(form['_id'], ObjectId):
        form['_id'] = str(form['_id'])

    if (user_role != "ADMIN"):
        personalForm = db.PersonalForm.find_one({"user_id": user_id, "form_id": form_id})
        if personalForm:
                form['hide_label'] = personalForm["hide_label"]
                if personalForm["layout"]:
                    layoutDict = {layout["i"] : layout for layout in personalForm["layout"]}
                    for elem in form["elements"]:
                        elem["layout"] = layoutDict[elem["element_id"]]
        else:
            form['hide_label'] = False

    return ApiResponse(code=200, response={"form": form})


@router.post("/personalize/")
async def personalize_element(
        entry: PersonalForm = Body(...),
        db: MongoDB = Depends(get_mongo_db)
):
    form = db.PersonalForm.find_one({"user_id": entry.user_id, "form_id": entry.form_id})
    if form:
        result = db.PersonalForm.update_one({"user_id": entry.user_id, "form_id":entry.form_id}, {"$set": entry.dict()})
        if result : return ApiResponse(code=200, response={"message": "Instance updated successfully"})
    else:
        result = await db.PersonalForm.insert_one(entry.dict())
        if result.inserted_id: return ApiResponse(code=200, response={"message": "Instance added successfully"})





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


@router.get("/get-entries/{user_id}/{form_id}")
async def get_entries(
        form_id: str,
        user_id: str,
        db: MongoDB = Depends(get_mongo_db)
):
    form = db.forms.find_one({"_id": ObjectId(form_id)})
    if form and form['user_id'] == user_id:
        data = list(db.entries.find({"form_id": form_id},{"_id": 0,"form_id": 0}))
        idToElement = dict((elem["element_id"], elem) for elem in form['elements'])
        outputData = []
        users = set()
        index = 1
        for document in data:
            if document['element_id']:
                if document['element_id'] in idToElement.keys():
                    output = {}
                    output["index"] = index
                    output["element_id"] = document['element_id']
                    output['element_type'] = idToElement[document['element_id']]['element_type']
                    output['label'] = idToElement[document['element_id']]['label']
                    output['user'] = document['user_id']
                    output['time'] = document['time']
                    output['value'] = document['value']
                    outputData.append(output)
                    users.add(document['user_id'])
                    index += 1

        return ApiResponse(code=200, response={"data": {"all":outputData, "count":len(outputData), "user_count":len(users)}})
    else:
        return ApiResponse(code=200, response={"data": []})
