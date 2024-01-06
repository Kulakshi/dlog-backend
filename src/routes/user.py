from fastapi import APIRouter, Query, Body, Depends
from mongodb import get_mongo_db, MongoDB
from src.models.commons import ApiResponse, UserEntry


router = APIRouter()



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

