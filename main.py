from fastapi import FastAPI
import pymongo

import mongodb
# from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from src.routes import elements, form, user
from fastapi.middleware.cors import CORSMiddleware
# from mongodb import MongoDB


app = FastAPI()
origins = ["*"] #add exact domain names where UI is hosted

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# mongo_db = MongoDB()
# app.dependency_overrides[mongodb.get_mongo_db()] = lambda: mongo_db

app.include_router(prefix="/elements", router=elements.router)
app.include_router(prefix="/form", router=form.router)
app.include_router(prefix="/user", router=user.router)

# from pymongo import MongoClient
# from src.config import MONGO_URI
#
# try:
#     client = MongoClient(MONGO_URI)
#     if client.server_info():
#         print("Connected to MongoDB successfully")
#     else:
#         print("Unable to connect to MongoDB")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
# finally:
#     client.close()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

