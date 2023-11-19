from fastapi import FastAPI
import pymongo

import mongodb
# from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from src.routes import elements, admin, user, elementTypes
from fastapi.middleware.cors import CORSMiddleware
from mongodb import MongoDB


app = FastAPI()
origins = ["*"] #add exact domain names where UI is hosted

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


mongo_db = MongoDB()
app.dependency_overrides[mongodb.get_mongo_db()] = lambda: mongo_db

app.include_router(prefix="/element-types", router=elementTypes.router)
app.include_router(prefix="/elements", router=elements.router)
app.include_router(prefix="/admin", router=admin.router)
app.include_router(prefix="/user", router=user.router)



@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

