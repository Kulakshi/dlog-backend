from fastapi import APIRouter, Query, Body, Depends
from mongodb import get_mongo_db, MongoDB
from src.models.commons import ApiResponse, UserEntry
from src.data.users import default_users
from bson import ObjectId


router = APIRouter()


def insert_default_users():
    db = MongoDB().get_database()
    for user in default_users:
        existing_element = db.user.find_one({"user_id": user.user_id})
        if not existing_element:
            db.user.insert_one(user.dict())
        print("Added default users")


@router.on_event("startup")
def on_startup():
    insert_default_users()


@router.get("/all/")
async def get_all_users(
        db: MongoDB = Depends(get_mongo_db)
):
    users = list(db.user.find())
    for user in users:
        if '_id' in user and isinstance(user['_id'], ObjectId):
            user['_id'] = str(user['_id'])
    return ApiResponse(code=200, response={"users": users})


@router.post("/login/")
async def login(
    user: UserEntry = Body(...),
    db: MongoDB = Depends(get_mongo_db)
):
    try:
        # Add user_id and time into login table
        login_data = {
            "user_id": user.user_id,
            "time": user.time,
        }
        db.login.insert_one(login_data)

        # if a user does not exists with user_id, team and project - add that to user table
        existing_user = db.user.find_one({
            "user_id": user.user_id,
            "team": user.team,
            "project": user.project
        })

        # If the user doesn't exist, add them to the user table
        if not existing_user:
            new_user = {
                "user_id": user.user_id,
                "team": user.team,
                "project": user.project
            }
            db.user.insert_one(new_user)

        return ApiResponse(code=200, response={"message": "Login successful"})
    except Exception as e:
        return ApiResponse(code=500, error= str(e))

